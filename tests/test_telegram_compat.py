import importlib
import inspect
import unittest


class TelegramCompatibilityTest(unittest.TestCase):
    def test_native_and_legacy_types_share_identity(self):
        import hikkatl, telethon

        self.assertIs(hikkatl, telethon)
        from hikkatl.tl.types import UserFull, Message
        from telethon.tl.types import Message as ModernMessage

        self.assertIs(Message, ModernMessage)
        self.assertIn("birthday", inspect.signature(UserFull).parameters)
        for suffix in (
            "tl.functions.users",
            "tl.functions.account",
            "errors.rpcerrorlist",
            "sessions",
        ):
            self.assertIs(
                importlib.import_module("hikkatl." + suffix),
                importlib.import_module("telethon." + suffix),
            )

    def test_existing_custom_emoji_markup_and_toggle(self):
        from hikkatl.extensions import html
        from telethon.tl.types import MessageEntityCustomEmoji

        html.CUSTOM_EMOJIS = True
        text, entities = html.parse('<emoji document_id="123">x</emoji>')
        self.assertEqual("x", text)
        self.assertIsInstance(entities[0], MessageEntityCustomEmoji)
        self.assertEqual(123, entities[0].document_id)
        try:
            html.CUSTOM_EMOJIS = False
            text, entities = html.parse('<emoji document_id="123">x</emoji>')
            self.assertEqual("x", text)
            self.assertEqual([], entities)
        finally:
            html.CUSTOM_EMOJIS = True

    def test_bundled_modules_import_with_new_api(self):
        # Existing security tests install lightweight translation stubs; use a clean interpreter.
        import subprocess
        import sys
        from pathlib import Path

        script = "import sys; sys.argv=['hikka','--no-web','--no-auth']; import hikka.main; import importlib,pkgutil; [importlib.import_module('hikka.modules.'+m.name) for m in pkgutil.iter_modules(['hikka/modules'])]"
        subprocess.run(
            [sys.executable, "-B", "-c", script],
            cwd=Path(__file__).resolve().parents[1],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def test_legacy_forum_methods_keep_keywords_and_positional_order(self):
        from hikkatl.tl.functions.channels import (
            GetForumTopicsRequest,
            CreateForumTopicRequest,
        )
        from telethon.tl.types import InputPeerChannel, InputChannel
        from telethon.tl.functions import messages

        peer = InputPeerChannel(123, 456)
        request = GetForumTopicsRequest(
            channel=peer, offset_date=None, offset_id=0, offset_topic=0, limit=20
        )
        self.assertIsInstance(request, messages.GetForumTopicsRequest)
        self.assertEqual(
            bytes(messages.GetForumTopicsRequest(peer, None, 0, 0, 20)), bytes(request)
        )
        positional = CreateForumTopicRequest(
            InputChannel(123, 456), "Topic", 42, 123, 456, None
        )
        self.assertEqual("Topic", positional.title)
        self.assertEqual(42, positional.icon_color)
        self.assertIsInstance(positional.peer, InputPeerChannel)
