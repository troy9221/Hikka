# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/troy9221/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

"""
Валидатор языковых пакетов (langpacks).

Проверяет YAML-файлы переводов в ``hikka/langpacks/*.yml`` без импорта самого
пакета ``hikka`` (чтобы обойти цепочку циклических импортов
``translations -> database -> ...``). Файлы читаются и парсятся напрямую тем же
самым загрузчиком ``ruamel.yaml``, который используется в проде
(см. hikka/translations.py). Если ruamel недоступен, используется PyYAML.

Что покрываем:
  * каждый .yml — синтаксически валидный YAML;
  * верхний уровень — словарь "модуль -> словарь строк";
  * все листовые значения строк — это скаляры (str/int/float/bool), а не
    случайно вложенные dict/list из-за ошибки отступа в YAML;
  * все языки из SUPPORTED_LANGUAGES имеют свой .yml;
  * позиционные плейсхолдеры ``{}``: в переводе их не должно быть БОЛЬШЕ, чем в
    эталонной английской строке — иначе ``str.format(*args)`` упадёт с
    ``IndexError`` в рантайме при показе строки пользователю.

Замечания по семантике данных (важно для понимания, почему проверки именно
такие):
  * Ключи внутри модуля могут быть числами (например ``unit_heta.404``): YAML
    парсит ``404:`` как int, а в проде translations.py формирует полный ключ
    через f-строку ``f"{prefix}{module}.{key}"``, где int корректно приводится
    к строке. Поэтому нечисловой тип ключа — не ошибка.
  * Модули с префиксом ``$`` (``$validators``, ``$inline``) — это общие наборы
    строк без человекочитаемого ``name``; отсутствие ``name`` у них нормально.
  * en.yml НЕ является полным надмножеством ключей: docstring-переводы
    (``_cls_doc``, ``_cmd_doc_*``) намеренно присутствуют только в неанглийских
    паках, т.к. английские док-строки берутся напрямую из Python-модулей. Поэтому
    "лишние" относительно en.yml ключи в переводах — это норма, а не ошибка.
"""

import re
from pathlib import Path

import pytest

try:
    from ruamel.yaml import YAML

    _yaml = YAML(typ="safe")

    def _load(text: str):
        return _yaml.load(text)

except ImportError:  # pragma: no cover - fallback, если ruamel не установлен
    import yaml as _pyyaml

    def _load(text: str):
        return _pyyaml.safe_load(text)


# Директория с langpack'ами относительно этого файла: tests/ -> ../hikka/langpacks
PACKS = Path(__file__).resolve().parent.parent / "hikka" / "langpacks"

# Ожидаемый набор языков. Держим локально, чтобы не импортировать
# hikka.translations (тянет requests/database и провоцирует циклический импорт).
SUPPORTED_LANGUAGES = {
    "en",
    "ru",
    "fr",
    "it",
    "de",
    "tr",
    "uz",
    "es",
    "kk",
    "tt",
}

# Позиционный плейсхолдер вида ``{}`` (пустые фигурные скобки).
# Экранированные ``{{`` / ``}}`` и именованные ``{key}`` (их обрабатывает
# translations.fmt отдельным механизмом) сюда не попадают.
_POSITIONAL_PLACEHOLDER = re.compile(r"(?<!\{)\{\}(?!\})")


def _yaml_files():
    return sorted(PACKS.glob("*.yml"))


def _positional_count(value: str) -> int:
    return len(_POSITIONAL_PLACEHOLDER.findall(str(value)))


def _load_pack(path: Path) -> dict:
    return _load(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def english_pack() -> dict:
    return _load_pack(PACKS / "en.yml")


def test_packs_directory_exists():
    assert PACKS.is_dir(), f"Директория langpacks не найдена: {PACKS}"


def test_english_reference_exists():
    assert (PACKS / "en.yml").is_file(), "Эталонный en.yml отсутствует"


def test_yaml_files_are_discovered():
    files = _yaml_files()
    assert files, "Не найдено ни одного .yml langpack"


@pytest.mark.parametrize(
    "path",
    _yaml_files(),
    ids=[p.stem for p in _yaml_files()],
)
def test_langpack_is_valid_yaml(path: Path):
    """Каждый файл парсится без ошибок и содержит непустой словарь."""
    data = _load_pack(path)
    assert isinstance(data, dict), f"{path.name}: верхний уровень не словарь"
    assert data, f"{path.name}: пустой langpack"


@pytest.mark.parametrize(
    "path",
    _yaml_files(),
    ids=[p.stem for p in _yaml_files()],
)
def test_langpack_structure(path: Path):
    """
    модуль -> {ключ: скаляр}.

    Значение каждой строки обязано быть скаляром (str/int/float/bool), а не
    вложенным dict/list. Вложенность почти всегда означает ошибку отступа в YAML,
    из-за которой строка "потеряется" и не покажется пользователю.
    """
    data = _load_pack(path)
    for module, strings in data.items():
        assert isinstance(module, str), f"{path.name}: имя модуля не строка: {module!r}"
        assert isinstance(strings, dict), (
            f"{path.name}: {module!r} должен быть словарём строк, "
            f"получено {type(strings).__name__}"
        )
        for key, value in strings.items():
            # Ключ может быть int (YAML парсит "404:" как число) — это валидно,
            # в проде он приводится к строке через f-строку. Запрещаем только
            # структурные типы значений.
            assert not isinstance(value, (dict, list)), (
                f"{path.name}: {module}.{key} — значение имеет тип "
                f"{type(value).__name__}; вероятно ошибка отступа в YAML"
            )


def test_all_supported_languages_present():
    """Для каждого языка из SUPPORTED_LANGUAGES существует .yml."""
    present = {p.stem for p in _yaml_files()}
    missing = SUPPORTED_LANGUAGES - present
    assert not missing, f"Отсутствуют langpack'и для языков: {sorted(missing)}"


def test_english_modules_have_name(english_pack: dict):
    """
    В эталоне у каждого обычного модуля есть человекочитаемое имя (ключ name).

    Модули с префиксом ``$`` (общие наборы строк вроде ``$validators``) — из
    проверки исключены: у них name отсутствует намеренно.
    """
    missing = [
        module
        for module, strings in english_pack.items()
        if not module.startswith("$") and "name" not in strings
    ]
    assert not missing, f"В en.yml у модулей нет ключа 'name': {missing}"


@pytest.mark.parametrize(
    "path",
    [p for p in _yaml_files() if p.stem != "en"],
    ids=[p.stem for p in _yaml_files() if p.stem != "en"],
)
def test_positional_placeholders_not_exceed_reference(path: Path, english_pack: dict):
    """
    Защита от рантайм-краша: перевод не должен содержать позиционных
    плейсхолдеров ``{}`` больше, чем эталонная строка. Лишний ``{}`` приведёт к
    ``IndexError`` в ``str.format(*args)`` при показе строки пользователю
    (число аргументов ``.format()`` в коде рассчитано на английский эталон).

    Сравниваем только те ключи, которые есть в обоих паках в рамках одного
    модуля; "осиротевшие" (docstring-переводы и т.п.) пропускаем.
    """
    data = _load_pack(path)
    problems = []
    for module, strings in data.items():
        reference = english_pack.get(module)
        if reference is None:
            continue
        for key, value in strings.items():
            if key == "name" or key not in reference:
                continue
            expected = _positional_count(reference[key])
            actual = _positional_count(value)
            if actual > expected:
                problems.append(
                    f"{module}.{key}: перевод содержит {actual} '{{}}' "
                    f"против {expected} в эталоне"
                )

    assert not problems, (
        f"{path.name}: перевод содержит лишние позиционные плейсхолдеры "
        f"(риск IndexError): {problems}"
    )
