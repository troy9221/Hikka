"""Unit tests for the self-contained Brainfuck interpreter in eval.py.

``hikka.modules.eval`` cannot currently be imported in isolation because the
package triggers a circular import (hikka.loader) outside of the normal
runtime bootstrap. Since the ``Brainfuck`` class is pure and dependency-free,
we load *only* its source out of the module file and exec it in an isolated
namespace. This keeps the test fast and free of Telegram/network deps.
"""

import ast
import pathlib

import pytest

EVAL_PATH = pathlib.Path(__file__).resolve().parent.parent / "hikka" / "modules" / "eval.py"


def _load_brainfuck():
    """Extract and compile just the ``Brainfuck`` class from eval.py."""
    source = EVAL_PATH.read_text(encoding="utf-8")
    module = ast.parse(source)

    class_node = next(
        (
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name == "Brainfuck"
        ),
        None,
    )
    if class_node is None:  # pragma: no cover - guards against future refactors
        pytest.skip("Brainfuck class not found in eval.py")

    namespace: dict = {"typing": __import__("typing")}
    isolated = ast.Module(body=[class_node], type_ignores=[])
    exec(compile(isolated, str(EVAL_PATH), "exec"), namespace)  # noqa: S102
    return namespace["Brainfuck"]


Brainfuck = _load_brainfuck()


def run(code: str) -> str:
    return Brainfuck().run(code)


def test_hello_world():
    program = (
        "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]"
        ">>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
    )
    assert run(program) == "Hello World!\n"


def test_empty_program_returns_empty():
    assert run("") == ""


def test_single_cell_increment_and_output():
    # 65 '+' then '.' -> chr(65) == 'A'
    assert run("+" * 65 + ".") == "A"


def test_unmatched_opening_bracket_reports_error():
    bf = Brainfuck()
    result = bf.run("[")
    assert result == ""
    assert bf.error  # unmatched brackets


def test_unmatched_closing_bracket_reports_error():
    bf = Brainfuck()
    result = bf.run("]")
    assert result == ""
    assert bf.error


def test_pointer_underflow_is_guarded():
    bf = Brainfuck()
    bf.run("<")
    assert bf.error == "pointer out of range at line 0, column 0"


def test_negative_memory_size_raises():
    with pytest.raises(ValueError):
        Brainfuck(memory_size=-1)
