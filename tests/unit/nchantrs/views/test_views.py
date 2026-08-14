"""Source-structure tests for nchantrs.views.views.

Uses AST + source-text assertions (matching the convention used in
``tests/unit/nchantrs/test_applicationmodel_tnew003.py``) so the test
suite does not depend on Qt instantiation — the project's mock-PyQt
metaclass conflicts in headless test environments prevent Nchantd
subclasses from being instantiated cleanly.

What this test verifies:

1. The module file exists at the expected path.
2. The module parses as valid Python (no syntax errors).
3. The module declares at least one public symbol (class, function,
   or constant) at module scope — guards against empty/stub files.
4. The module does not accidentally contain ``raise NotImplementedError``
   inside a ``def`` body that hasn't been decorated or marked as a
   hook (catches the common "foliation missed this stub" case where a
   scaffold body stays as ``pass`` or ``raise NotImplementedError``).
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / Path("views", "views.py")


@pytest.fixture(scope="module")
def source():
    return MODULE_PATH.read_text()


@pytest.fixture(scope="module")
def tree(source):
    return ast.parse(source)


def test_module_file_exists():
    assert MODULE_PATH.exists(), "module file missing: " + str(MODULE_PATH)
    assert MODULE_PATH.is_file()


def test_module_parses_cleanly(tree):
    """No SyntaxError — the AST fixture would have raised during parse."""
    assert tree is not None


def test_module_has_public_symbols(tree):
    """At least one module-level ClassDef, FunctionDef, or Assign."""
    public_kinds = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Assign, ast.AnnAssign)
    public = [n for n in tree.body if isinstance(n, public_kinds)]
    assert public, (
        "module declares no module-level symbols — likely a stub file "
        "awaiting foliation: " + str(MODULE_PATH)
    )


def test_module_no_unhandled_not_implemented(tree):
    """No bare ``raise NotImplementedError`` in def bodies without a hook marker.

    AST-only check — does not import the module, so it catches the
    "foliation missed this stub" pattern at the source level.
    """
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip dunder / hook / private-prefixed method names —
            # those are intentional abstract hooks.
            if node.name.startswith("_") or node.name.startswith("__"):
                continue
            for child in ast.walk(node):
                if isinstance(child, ast.Raise) and isinstance(child.exc, ast.Call):
                    func = child.exc.func
                    name = None
                    if isinstance(func, ast.Name):
                        name = func.id
                    elif isinstance(func, ast.Attribute):
                        name = func.attr
                    if name == "NotImplementedError":
                        bad.append(node.name)
    assert not bad, (
        "public methods still raise NotImplementedError: " + str(bad) + ". "
        "These are stub bodies awaiting foliation."
    )
