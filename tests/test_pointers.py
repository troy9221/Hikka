"""Unit tests for hikka.pointers.

These tests use a lightweight in-memory fake database that mimics the
subset of the real :class:`hikka.database.Database` API that pointers rely on
(``get`` and ``set``). This keeps the tests free of Telegram/network deps.
"""

import typing

import pytest

from hikka.pointers import PointerDict, PointerList


class FakeDatabase:
    """Minimal in-memory stand-in for hikka.database.Database."""

    def __init__(self) -> None:
        self._store: typing.Dict[str, typing.Dict[str, typing.Any]] = {}

    def get(self, owner: str, key: str, default: typing.Any = None) -> typing.Any:
        try:
            return self._store[owner][key]
        except KeyError:
            return default

    def set(self, owner: str, key: str, value: typing.Any) -> bool:
        self._store.setdefault(owner, {})[key] = value
        return True


@pytest.fixture
def db() -> FakeDatabase:
    return FakeDatabase()


# --- PointerList -----------------------------------------------------------


def test_pointer_list_initializes_from_default(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [1, 2, 3])
    assert list(ptr) == [1, 2, 3]


def test_pointer_list_append_persists(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [])
    ptr.append("a")
    assert db.get("mod", "key") == ["a"]


def test_pointer_list_extend_and_pop_persist(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [])
    ptr.extend([1, 2, 3])
    assert db.get("mod", "key") == [1, 2, 3]

    popped = ptr.pop()
    assert popped == 3
    assert db.get("mod", "key") == [1, 2]


def test_pointer_list_remove_persists(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", ["x", "y"])
    ptr.remove("x")
    assert db.get("mod", "key") == ["y"]


def test_pointer_list_setitem_persists(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [0, 0])
    ptr[1] = 42
    assert db.get("mod", "key") == [0, 42]


def test_pointer_list_data_setter_replaces(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [1])
    ptr.data = [9, 8, 7]
    assert db.get("mod", "key") == [9, 8, 7]
    assert ptr.data == [9, 8, 7]


def test_pointer_list_tolist_reads_from_db(db: FakeDatabase):
    ptr = PointerList(db, "mod", "key", [])
    ptr.append("z")
    assert ptr.tolist() == ["z"]


# --- PointerDict -----------------------------------------------------------


def test_pointer_dict_initializes_from_default(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {"a": 1})
    assert dict(ptr) == {"a": 1}


def test_pointer_dict_setitem_persists(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {})
    ptr["a"] = 1
    assert db.get("mod", "key") == {"a": 1}


def test_pointer_dict_delitem_persists(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {"a": 1, "b": 2})
    del ptr["a"]
    assert db.get("mod", "key") == {"b": 2}


def test_pointer_dict_update_persists(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {})
    ptr.update({"x": 10, "y": 20})
    assert db.get("mod", "key") == {"x": 10, "y": 20}


def test_pointer_dict_pop_persists(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {"a": 1, "b": 2})
    value = ptr.pop("a")
    assert value == 1
    assert db.get("mod", "key") == {"b": 2}


def test_pointer_dict_setdefault_persists(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {})
    assert ptr.setdefault("a", 5) == 5
    assert db.get("mod", "key") == {"a": 5}


def test_pointer_dict_bool_reflects_db(db: FakeDatabase):
    empty = PointerDict(db, "mod", "empty", {})
    assert not bool(empty)

    filled = PointerDict(db, "mod", "filled", {"a": 1})
    assert bool(filled)


def test_pointer_dict_todict_reads_from_db(db: FakeDatabase):
    ptr = PointerDict(db, "mod", "key", {})
    ptr["k"] = "v"
    assert ptr.todict() == {"k": "v"}
