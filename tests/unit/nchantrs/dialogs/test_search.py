"""Source-structure tests for nchantrs.dialogs.search."""
import ast
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "dialogs" / "search.py"


@pytest.fixture(scope="module")
def source():
    return MODULE_PATH.read_text()


@pytest.fixture(scope="module")
def tree(source):
    return ast.parse(source)


def test_module_file_exists():
    assert MODULE_PATH.exists()
    assert MODULE_PATH.is_file()


def test_module_parses_cleanly(tree):
    assert tree is not None


def test_module_has_public_symbols(tree):
    public_kinds = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.Assign, ast.AnnAssign)
    public = [n for n in tree.body if isinstance(n, public_kinds)]
    assert public, "no module-level symbols"


def test_find_sigil_class_exists(tree):
    classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    assert "NchantdFindSigil" in classes


def test_find_sigil_has_init_methods(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NchantdFindSigil":
            method_names = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            for method in ["initModel", "initView", "initWidget"]:
                assert method in method_names, f"Missing method: {method}"
            return
    pytest.fail("NchantdFindSigil class not found")
