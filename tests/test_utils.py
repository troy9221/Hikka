"""Unit-тесты для чистых функций из hikka.utils.

Тестируются только функции, не требующие Telegram-клиента, сети или
работающего event loop: обработка аргументов, экранирование, простые
преобразования данных.
"""

import pytest

from hikka import utils


# ---------------------------------------------------------------------------
# escape_html / escape_quotes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("<b>", "&lt;b&gt;"),
        ("a & b", "a &amp; b"),
        ("<a href='x'>", "&lt;a href='x'&gt;"),
        ("plain", "plain"),
        ("", ""),
    ],
)
def test_escape_html(raw, expected):
    assert utils.escape_html(raw) == expected


def test_escape_html_ampersand_first():
    # & должен экранироваться первым, чтобы не поломать уже экранированные < >
    assert utils.escape_html("<&>") == "&lt;&amp;&gt;"


def test_escape_html_non_str():
    assert utils.escape_html(123) == "123"


def test_escape_quotes():
    assert utils.escape_quotes('say "hi" & <bye>') == "say &quot;hi&quot; &amp; &lt;bye&gt;"


# ---------------------------------------------------------------------------
# get_args / get_args_raw / get_args_split_by
# ---------------------------------------------------------------------------


def test_get_args_raw_simple():
    assert utils.get_args_raw(".cmd hello world") == "hello world"


def test_get_args_raw_no_args():
    assert utils.get_args_raw(".cmd") == ""


def test_get_args_raw_empty():
    # Пустая строка -> falsy, функция возвращает False
    assert utils.get_args_raw("") is False


def test_get_args_simple():
    assert utils.get_args(".cmd a b c") == ["a", "b", "c"]


def test_get_args_quoted():
    # shlex учитывает кавычки
    assert utils.get_args('.cmd "a b" c') == ["a b", "c"]


def test_get_args_no_args():
    assert utils.get_args(".cmd") == []


def test_get_args_unbalanced_quote_fallback():
    assert utils.get_args('.cmd "unclosed') == '"unclosed'


def test_get_args_split_by():
    assert utils.get_args_split_by(".cmd a | b | c", "|") == ["a", "b", "c"]


def test_get_args_split_by_skips_empty():
    assert utils.get_args_split_by(".cmd a || b", "|") == ["a", "b"]


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------


def test_merge_overrides():
    assert utils.merge({"a": 1}, {"a": 0, "b": 2}) == {"a": 1, "b": 2}


def test_merge_nested_dicts():
    a = {"x": {"y": 1}}
    b = {"x": {"z": 2}}
    result = utils.merge(a, b)
    assert result == {"x": {"y": 1, "z": 2}}


def test_merge_lists_union():
    result = utils.merge({"k": [1, 2]}, {"k": [2, 3]})
    assert sorted(result["k"]) == [1, 2, 3]


# ---------------------------------------------------------------------------
# chunks
# ---------------------------------------------------------------------------


def test_chunks_even():
    assert utils.chunks([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_chunks_uneven():
    assert utils.chunks([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_chunks_empty():
    assert utils.chunks([], 3) == []


# ---------------------------------------------------------------------------
# array_sum
# ---------------------------------------------------------------------------


def test_array_sum():
    assert utils.array_sum([[1, 2], [3], [4, 5]]) == [1, 2, 3, 4, 5]


def test_array_sum_empty():
    assert utils.array_sum([]) == []


# ---------------------------------------------------------------------------
# rand
# ---------------------------------------------------------------------------


def test_rand_length():
    assert len(utils.rand(16)) == 16


def test_rand_charset():
    allowed = set("abcdefghijklmnopqrstuvwxyz1234567890")
    assert set(utils.rand(100)) <= allowed


def test_rand_zero():
    assert utils.rand(0) == ""


# ---------------------------------------------------------------------------
# check_url
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("url", "valid"),
    [
        ("https://example.com", True),
        ("http://a.b/c?d=e", True),
        ("not a url", False),
        ("", False),
        ("ftp://host/file", True),
    ],
)
def test_check_url(url, valid):
    assert utils.check_url(url) is valid


# ---------------------------------------------------------------------------
# is_serializable
# ---------------------------------------------------------------------------


def test_is_serializable_true():
    assert utils.is_serializable({"a": [1, 2], "b": "x"}) is True


def test_is_serializable_false():
    assert utils.is_serializable({1, 2, 3}) is False


def test_is_serializable_object():
    assert utils.is_serializable(object()) is False


# ---------------------------------------------------------------------------
# get_lang_flag
# ---------------------------------------------------------------------------


def test_get_lang_flag_valid():
    # 2-буквенный код -> regional indicator symbols
    flag = utils.get_lang_flag("us")
    assert flag == "🇺🇸"


def test_get_lang_flag_invalid_length():
    # Не 2 буквы -> возвращается исходная строка
    assert utils.get_lang_flag("english") == "english"


# ---------------------------------------------------------------------------
# remove_html
# ---------------------------------------------------------------------------


def test_remove_html_basic():
    assert utils.remove_html("<b>bold</b> and <i>italic</i>") == "bold and italic"


def test_remove_html_link():
    assert utils.remove_html('<a href="x">text</a>') == "text"


def test_remove_html_keep_emojis():
    # keep_emojis=True не должен удалять <emoji> теги
    text = '<emoji document_id="1">😀</emoji>'
    assert utils.remove_html(text, keep_emojis=True) == text


def test_remove_html_strip_emojis():
    text = '<emoji document_id="1">😀</emoji>'
    assert utils.remove_html(text) == "😀"


# ---------------------------------------------------------------------------
# get_dir
# ---------------------------------------------------------------------------


def test_get_dir_returns_abs_dir():
    import os

    result = utils.get_dir(utils.__file__)
    assert os.path.isabs(result)
    assert os.path.isdir(result)
