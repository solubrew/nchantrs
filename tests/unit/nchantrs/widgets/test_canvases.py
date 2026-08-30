"""Source-structure tests for nchantrs.widgets.canvases.canvases."""
import ast
from pathlib import Path
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MODULE_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "canvases" / "canvases.py"


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


def test_canvas_classes_exist(tree):
    classes = {n.name for n in tree.body if isinstance(n, ast.ClassDef)}
    expected = {
        "ThreeJSWidget", "NchantdCanvas", "NchantdPaintCanvas", "NchantdGameCanvas",
        "NchantdMapCanvas", "NchantdWireFrameCanvas", "NchantdSpace",
    }
    assert expected.issubset(classes), f"Missing classes: {expected - classes}"


def test_nchantd_canvas_has_scene(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NchantdCanvas":
            method_names = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            for method in ["initView", "add_item", "setDisplayPixmap"]:
                assert method in method_names, f"Missing method: {method}"
            return
    pytest.fail("NchantdCanvas class not found")


def test_paint_canvas_has_draw_methods(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "NchantdPaintCanvas":
            method_names = {n.name for n in node.body if isinstance(n, ast.FunctionDef)}
            for method in ["clear", "select_pen_color", "select_pen_width"]:
                assert method in method_names, f"Missing method: {method}"
            return
    pytest.fail("NchantdPaintCanvas class not found")
