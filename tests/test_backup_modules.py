import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace as NS, ModuleType
from unittest.mock import AsyncMock, patch
import unittest
import zipfile


class BackupModulesTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        import importlib.util

        package = ModuleType("backup_hikka")
        package.__path__ = []
        modules = ModuleType("backup_hikka.modules")
        modules.__path__ = []
        inline = ModuleType("backup_hikka.inline")
        inline.__path__ = []
        inline_types = ModuleType("backup_hikka.inline.types")
        inline_types.BotInlineCall = object

        class StopLoop(Exception):
            pass

        package.loader = NS(
            Module=object,
            tds=lambda cls: cls,
            owner=lambda f: f,
            command=lambda **k: lambda f: f,
            loop=lambda **k: lambda f: NS(func=f),
            StopLoop=StopLoop,
        )
        package.utils = NS(
            answer=AsyncMock(),
            escape_html=lambda value: value,
            check_url=lambda value: value.startswith("https://"),
        )
        source = Path(__file__).resolve().parents[1] / "hikka/modules/hikka_backup.py"
        message_types = ModuleType("hikkatl.tl.types")
        message_types.Message = object
        with patch.dict(
            sys.modules,
            {
                "backup_hikka": package,
                "backup_hikka.modules": modules,
                "backup_hikka.inline": inline,
                "backup_hikka.inline.types": inline_types,
                "hikkatl.tl.types": message_types,
            },
        ):
            spec = importlib.util.spec_from_file_location(
                "backup_hikka.modules.backup", source
            )
            self.module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.module)
        self.mod = self.module.HikkaBackupMod()
        self.mod.strings = lambda key: self.module.HikkaBackupMod.strings[key]
        self.mod.get_prefix = lambda: "!"
        self.mod._client = NS(send_file=AsyncMock())
        self.mod._backup_channel = "existing-backup-group"
        self.mod.tg_id = 123

        class Database(dict):
            def save(self):
                return True

            def process_db_autofix(self, data):
                return isinstance(data, dict)

        self.mod._db = Database({"settings": {"example": True}})
        self.mod.allmodules = NS(modules=[])
        self.urls = {"RemoteMod": "https://example.com/remote.py"}

        class LoaderMod:
            def get(inner, key, default=None):
                return self.mod._db.get("LoaderMod", {}).get(key, default)

            def set(inner, key, value):
                self.mod._db.setdefault("LoaderMod", {})[key] = value

        self.registry = LoaderMod()
        self.registry.set("loaded_modules", self.urls.copy())
        self.mod.lookup = lambda name: self.registry
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.patch = patch.object(
            self.module.loader, "LOADED_MODULES_DIR", str(self.directory), create=True
        )
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.module.loader.LOADED_MODULES_PATH = self.directory
        (self.directory / "MineMod_123.py").write_text("local source", encoding="utf-8")
        (self.directory / "OtherMod_456.py").write_text(
            "other account", encoding="utf-8"
        )
        (self.directory / "session.session").write_bytes(b"excluded")

    def test_archive_contains_own_sources_and_urls_only(self):
        with zipfile.ZipFile(self.mod._modules_backup()) as archive:
            self.assertEqual(
                {"MineMod_123.py", "db_mods.json"}, set(archive.namelist())
            )
            self.assertEqual(b"local source", archive.read("MineMod_123.py"))
            self.assertEqual(
                {"RemoteMod": "https://example.com/remote.py"},
                json.loads(archive.read("db_mods.json")),
            )

    def test_runtime_module_source_is_not_lost(self):
        namespace = ModuleType("runtime_module")
        namespace.__loader__ = NS(data=b"complete runtime source")
        cls = type("RuntimeMod", (), {"__module__": "runtime_module"})
        instance = cls()
        instance.__origin__ = "https://example.com/runtime.py"
        self.mod.allmodules.modules = [instance]
        with patch.dict(sys.modules, {"runtime_module": namespace}), zipfile.ZipFile(
            self.mod._modules_backup()
        ) as archive:
            self.assertEqual(
                b"complete runtime source", archive.read("RuntimeMod_123.py")
            )

    async def test_missing_runtime_source_does_not_publish_incomplete_backup(self):
        cls = type("MissingMod", (), {"__module__": "missing_runtime_namespace"})
        module = cls()
        module.__origin__ = "https://example.com/missing.py"
        self.mod.allmodules.modules = [module]
        with self.assertRaises(ValueError):
            await self.mod._send_backup()
        self.mod._client.send_file.assert_not_awaited()

    async def test_full_backup_sends_one_archive_with_three_restore_commands(self):
        await self.mod._send_backup()
        calls = self.mod._client.send_file.await_args_list
        self.assertEqual(1, len(calls))
        self.assertTrue(all(c.args[0] == "existing-backup-group" for c in calls))
        self.assertIn("!restoredb", calls[0].kwargs["caption"])
        self.assertIn("!restoremods", calls[0].kwargs["caption"])
        self.assertIn("!restorebackup", calls[0].kwargs["caption"])
        with zipfile.ZipFile(calls[0].args[1]) as archive:
            self.assertIn("MineMod_123.py", archive.namelist())
            self.assertEqual(self.mod._db, json.loads(archive.read("hikka-db.json")))

    async def test_archive_failure_does_not_send_a_config_only_backup(self):
        with patch.object(
            self.mod, "_modules_backup", side_effect=OSError("unreadable")
        ):
            with self.assertRaises(OSError):
                await self.mod._send_backup()
        self.mod._client.send_file.assert_not_awaited()

    async def test_scheduler_marks_success_only_after_archive_delivery(self):
        self.mod.get = lambda key: {"period": 60, "last_backup": 10}.get(key)
        saved = []
        self.mod.set = lambda *args: saved.append(args)
        self.mod._client.send_file.side_effect = OSError("offline")
        with patch.object(self.module.asyncio, "sleep", new=AsyncMock()), patch.object(
            self.module.time, "time", return_value=1_800_000_000
        ):
            await self.mod.handler.func(self.mod)
        # The archive is built and delivery is attempted, but a failed send is not recorded.
        self.mod._client.send_file.assert_awaited_once()
        self.assertEqual([], saved)

    def test_full_restore_recovers_config_and_module_sources(self):
        data = self.mod._full_backup().getvalue()
        self.mod._db["settings"] = {"example": False}
        (self.directory / "MineMod_123.py").write_text("changed")
        self.mod._restore_payload(data, configuration=True, modules=True)
        self.assertEqual({"example": True}, self.mod._db["settings"])
        self.assertEqual(
            b"local source", (self.directory / "MineMod_123.py").read_bytes()
        )
        self.assertEqual(self.urls, self.registry.get("loaded_modules"))

    def test_config_only_restore_leaves_module_files_unchanged(self):
        data = self.mod._full_backup().getvalue()
        self.mod._db["settings"] = {"example": False}
        self.registry.set("loaded_modules", {"NewMod": "https://example.com/new.py"})
        (self.directory / "MineMod_123.py").write_text("changed")
        self.mod._restore_payload(data, configuration=True)
        self.assertEqual({"example": True}, self.mod._db["settings"])
        self.assertEqual(b"changed", (self.directory / "MineMod_123.py").read_bytes())
        self.assertEqual(
            {"NewMod": "https://example.com/new.py"},
            self.registry.get("loaded_modules"),
        )

    def test_modules_only_restore_preserves_other_settings(self):
        data = self.mod._full_backup().getvalue()
        self.mod._db["settings"] = {"example": False}
        (self.directory / "MineMod_123.py").write_text("changed")
        self.mod._restore_payload(data, modules=True)
        self.assertEqual({"example": False}, self.mod._db["settings"])
        self.assertEqual(
            b"local source", (self.directory / "MineMod_123.py").read_bytes()
        )
        self.assertFalse((self.directory / "hikka-db.json").exists())

    def test_legacy_json_and_module_zip_remain_restorable(self):
        config = self.mod._database_backup().getvalue()
        modules = self.mod._modules_backup().getvalue()
        self.mod._db["settings"] = {"example": False}
        self.mod._restore_payload(config, configuration=True)
        self.assertTrue(self.mod._db["settings"]["example"])
        self.mod._restore_payload(modules, modules=True)

    def test_invalid_archive_is_rejected_before_any_changes(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, "w") as archive:
            archive.writestr(
                "hikka-db.json", json.dumps({"settings": {"example": False}})
            )
            archive.writestr("db_mods.json", "{}")
            archive.writestr("../Outside_123.py", "bad")
        with self.assertRaises(ValueError):
            self.mod._restore_payload(data.getvalue(), configuration=True, modules=True)
        self.assertTrue(self.mod._db["settings"]["example"])
        self.assertEqual(
            b"local source", (self.directory / "MineMod_123.py").read_bytes()
        )

    def test_save_failure_rolls_back_config_and_files(self):
        data = self.mod._full_backup().getvalue()
        self.mod._db["settings"] = {"example": False}
        (self.directory / "MineMod_123.py").write_text("changed")
        from unittest.mock import Mock

        self.mod._db.save = Mock(side_effect=[False, True])
        with self.assertRaises(OSError):
            self.mod._restore_payload(data, configuration=True, modules=True)
        self.assertEqual({"example": False}, self.mod._db["settings"])
        self.assertEqual(b"changed", (self.directory / "MineMod_123.py").read_bytes())
