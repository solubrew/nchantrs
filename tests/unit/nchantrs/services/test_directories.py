"""Source-structure tests for nchantrs.services.directories."""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "services" / "directories.py"


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


def test_directory_classes_exist(tree):
    classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    expected = {"SandboxDirectories", "PeerDirectories", "SystemDirectories", "UserDirectories"}
    assert expected.issubset(classes), f"Missing classes: {expected - classes}"
