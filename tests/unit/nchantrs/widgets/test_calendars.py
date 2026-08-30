"""Source-structure tests for nchantrs.widgets.calendars.calendars."""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "calendars" / "calendars.py"

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

def test_calendar_classes_exist(tree):
    classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    expected = {"NchantdCalendar", "NchantdDateTimeSelect", "NchantdDateTimeGroup",
                 "NchantdDateSelect", "NchantdDateIterate", "NchantdEventsList", "NchantdTimeSelect"}
    assert expected.issubset(classes), f"Missing classes: {expected - classes}"

def test_calendar_initView_uses_match(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NchantdCalendar":
            for child in node.body:
                if isinstance(child, ast.FunctionDef) and child.name == "initView":
                    match_found = any(isinstance(s, ast.Match) for s in ast.walk(child))
                    assert match_found, "NchantdCalendar.initView should use match statement for scope"
                    return
    pytest.fail("NchantdCalendar.initView not found")
