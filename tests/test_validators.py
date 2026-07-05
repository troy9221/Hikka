import sys
import types

import pytest


def _install_translations_stub() -> None:
    """Ставит заглушку hikka.translations в sys.modules (idempotent)."""
    if "hikka.translations" in sys.modules and getattr(
        sys.modules["hikka.translations"], "_is_test_stub", False
    ):
        return

    stub = types.ModuleType("hikka.translations")
    stub._is_test_stub = True
    stub.SUPPORTED_LANGUAGES = ["en", "ru"]

    class _FakeTranslator:
        # doc-тексты не участвуют в проверках значений, поэтому возвращаем
        # тривиальный словарь. .format(**kwargs) на строке без плейсхолдеров
        # просто вернёт её саму.
        @staticmethod
        def getdict(key: str, **kwargs) -> dict:
            return {"en": "doc", "ru": "док"}

    stub.translator = _FakeTranslator()
    sys.modules["hikka.translations"] = stub


_install_translations_stub()

from hikka import validators  # noqa: E402
from hikka.validators import ValidationError  # noqa: E402


# ---------------------------------------------------------------------------
# Boolean
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("value", ["True", "1", 1, True, "yes", "on", "y"])
def test_boolean_true(value):
    assert validators.Boolean().validate(value) is True


@pytest.mark.parametrize("value", ["False", "0", 0, False, "no", "off", "n"])
def test_boolean_false(value):
    assert validators.Boolean().validate(value) is False


def test_boolean_invalid():
    with pytest.raises(ValidationError):
        validators.Boolean().validate("maybe")


# ---------------------------------------------------------------------------
# Integer
# ---------------------------------------------------------------------------


def test_integer_basic():
    assert validators.Integer().validate("42") == 42


def test_integer_strips_whitespace():
    assert validators.Integer().validate("  7 ") == 7


def test_integer_not_a_number():
    with pytest.raises(ValidationError):
        validators.Integer().validate("abc")


def test_integer_below_minimum():
    with pytest.raises(ValidationError):
        validators.Integer(minimum=10).validate("5")


def test_integer_above_maximum():
    with pytest.raises(ValidationError):
        validators.Integer(maximum=10).validate("15")


def test_integer_within_range():
    assert validators.Integer(minimum=0, maximum=100).validate("50") == 50


def test_integer_wrong_digits():
    with pytest.raises(ValidationError):
        validators.Integer(digits=3).validate("42")


def test_integer_correct_digits():
    assert validators.Integer(digits=3).validate("123") == 123


# ---------------------------------------------------------------------------
# Float
# ---------------------------------------------------------------------------


def test_float_basic():
    assert validators.Float().validate("3.14") == 3.14


def test_float_comma_as_dot():
    assert validators.Float().validate("2,5") == 2.5


def test_float_invalid():
    with pytest.raises(ValidationError):
        validators.Float().validate("not-a-float")


def test_float_below_minimum():
    with pytest.raises(ValidationError):
        validators.Float(minimum=1.0).validate("0.5")


def test_float_above_maximum():
    with pytest.raises(ValidationError):
        validators.Float(maximum=1.0).validate("2.0")


# ---------------------------------------------------------------------------
# Choice / MultiChoice
# ---------------------------------------------------------------------------


def test_choice_valid():
    assert validators.Choice([1, 2, 3]).validate(2) == 2


def test_choice_invalid():
    with pytest.raises(ValidationError):
        validators.Choice([1, 2, 3]).validate(4)


def test_multichoice_valid():
    result = validators.MultiChoice(["a", "b", "c"]).validate(["a", "c"])
    assert set(result) == {"a", "c"}


def test_multichoice_single_value_wrapped():
    result = validators.MultiChoice(["a", "b"]).validate("a")
    assert result == ["a"]


def test_multichoice_invalid_item():
    with pytest.raises(ValidationError):
        validators.MultiChoice(["a", "b"]).validate(["a", "z"])


# ---------------------------------------------------------------------------
# String
# ---------------------------------------------------------------------------


def test_string_converts_to_str():
    assert validators.String().validate(123) == "123"


def test_string_fixed_length_ok():
    assert validators.String(length=3).validate("abc") == "abc"


def test_string_fixed_length_fail():
    with pytest.raises(ValidationError):
        validators.String(length=3).validate("abcd")


def test_string_min_len_fail():
    with pytest.raises(ValidationError):
        validators.String(min_len=5).validate("ab")


def test_string_max_len_fail():
    with pytest.raises(ValidationError):
        validators.String(max_len=2).validate("abcd")


# ---------------------------------------------------------------------------
# Series
# ---------------------------------------------------------------------------


def test_series_splits_string():
    assert validators.Series().validate("a, b, c") == ["a", "b", "c"]


def test_series_accepts_list():
    assert validators.Series().validate(["x", "y"]) == ["x", "y"]


def test_series_min_len_fail():
    with pytest.raises(ValidationError):
        validators.Series(min_len=3).validate("a,b")


def test_series_max_len_fail():
    with pytest.raises(ValidationError):
        validators.Series(max_len=2).validate("a,b,c")


def test_series_fixed_len_ok():
    assert validators.Series(fixed_len=2).validate("a,b") == ["a", "b"]


def test_series_with_inner_validator():
    result = validators.Series(validators.Integer()).validate("1, 2, 3")
    assert result == [1, 2, 3]


def test_series_inner_validator_fail():
    with pytest.raises(ValidationError):
        validators.Series(validators.Integer()).validate("1, x, 3")


# ---------------------------------------------------------------------------
# TelegramID
# ---------------------------------------------------------------------------


def test_telegram_id_basic():
    assert validators.TelegramID().validate("12345") == 12345


def test_telegram_id_strips_minus_100():
    assert validators.TelegramID().validate("-1001234567890") == 1234567890


def test_telegram_id_invalid():
    with pytest.raises(ValidationError):
        validators.TelegramID().validate("not-an-id")


# ---------------------------------------------------------------------------
# Union
# ---------------------------------------------------------------------------


def test_union_first_match():
    v = validators.Union(validators.Integer(), validators.Boolean())
    assert v.validate("10") == 10


def test_union_second_match():
    v = validators.Union(validators.Integer(), validators.Boolean())
    assert v.validate("yes") is True


def test_union_no_match():
    v = validators.Union(validators.Integer(minimum=100))
    with pytest.raises(ValidationError):
        v.validate("hello")


# ---------------------------------------------------------------------------
# NoneType
# ---------------------------------------------------------------------------


def test_none_type_empty_returns_none():
    assert validators.NoneType().validate("") is None


def test_none_type_nonempty_raises():
    with pytest.raises(ValidationError):
        validators.NoneType().validate("something")


# ---------------------------------------------------------------------------
# Hidden (делегирует внутреннему валидатору)
# ---------------------------------------------------------------------------


def test_hidden_delegates():
    assert validators.Hidden(validators.Integer()).validate("7") == 7


def test_hidden_default_is_string():
    assert validators.Hidden().validate(5) == "5"


# ---------------------------------------------------------------------------
# RegExp
# ---------------------------------------------------------------------------


def test_regexp_match():
    assert validators.RegExp(r"^\d+$").validate("123") == "123"


def test_regexp_no_match():
    with pytest.raises(ValidationError):
        validators.RegExp(r"^\d+$").validate("abc")


def test_regexp_invalid_pattern_raises_on_construction():
    # RegExp оборачивает re.error в Exception с текстом "... is not a valid regex"
    with pytest.raises(Exception, match="not a valid regex"):
        validators.RegExp(r"(")


# ---------------------------------------------------------------------------
# Link
# ---------------------------------------------------------------------------


def test_link_valid():
    assert validators.Link().validate("https://example.com") == "https://example.com"


def test_link_invalid():
    with pytest.raises(ValidationError):
        validators.Link().validate("not a url")


# ---------------------------------------------------------------------------
# EntityLike
# ---------------------------------------------------------------------------


def test_entitylike_adds_at_sign():
    assert validators.EntityLike().validate("durov") == "@durov"


def test_entitylike_keeps_at_sign():
    assert validators.EntityLike().validate("@durov") == "@durov"


def test_entitylike_strips_url():
    assert validators.EntityLike().validate("https://t.me/durov") == "@durov"
