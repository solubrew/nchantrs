"""Source-structure tests for nchantrs.widgets.launch."""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "launch.py"


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


def test_launch_module_imports_expected(tree):
    """Module should import NchantdNewApplicationWizard from wizards.accounts."""
    source_text = MODULE_PATH.read_text()
    assert "NchantdNewApplicationWizard" in source_text
    assert "wizards.accounts" in source_text
