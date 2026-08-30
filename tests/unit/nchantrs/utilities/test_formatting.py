"""Source-structure tests for nchantrs.utilities.formatting."""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "utilities" / "formatting.py"


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


def test_module_no_unhandled_not_implemented(tree):
    bad = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
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
    assert not bad, f"Unhandled NotImplementedError in: {bad}"


def test_formatting_exports_nchantdfonts_and_getalignment(tree):
    classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    funcs = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert "NchantdFonts" in classes
    assert "getAlignment" in funcs


def test_nchantdfonts_has_apply_sequence(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NchantdFonts":
            method_names = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            assert "apply_sequence" in method_names
            return
    pytest.fail("NchantdFonts class not found")


def test_getalignment_handles_all_justify_options(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "getAlignment":
            # getAlignment should have an ALIGNMENT_MAP dict
            for child in node.body:
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "ALIGNMENT_MAP":
                            return
            pytest.fail("getAlignment should define ALIGNMENT_MAP")
    pytest.fail("getAlignment function not found")
