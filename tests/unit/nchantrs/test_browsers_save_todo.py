"""Tests for the 2 round-2 TODO fixes:
1. NchantdWebViewer.save and _to_dict (browsers.py:484)
2. NchantdCloak._detect_display_system stray TODO (applications.py:317)

Uses AST + source-text assertions.
"""
import pytest
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BROWSERS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "browsers" / "browsers.py"
APPS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "applications" / "applications.py"


@pytest.fixture(scope="module")
def browsers_source():
    return BROWSERS_PATH.read_text()


@pytest.fixture(scope="module")
def browsers_ast(browsers_source):
    return ast.parse(browsers_source)


@pytest.fixture(scope="module")
def apps_source():
    return APPS_PATH.read_text()


@pytest.fixture(scope="module")
def apps_ast(apps_source):
    return ast.parse(apps_source)


def _find_class(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_method(class_node, name):
    if class_node is None:
        return None
    for child in class_node.body:
        if isinstance(child, ast.FunctionDef) and child.name == name:
            return child
    return None


# ---------- NchantdWebViewer.save ----------

def test_save_method_no_todo(browsers_ast):
    """The TODO at the top of save() is removed."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "save")
    assert method is not None
    body_src = ast.unparse(method)
    assert "TODO implement basic save function" not in body_src


def test_save_method_has_docstring(browsers_ast):
    """The save method should have a docstring explaining the persistence."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "save")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "save" in docstring.lower() or "snapshot" in docstring.lower()


def test_save_method_marks_app_model_changed(browsers_ast):
    """The save should mark app.model.has_changed = True so the app
    notices the state change."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "save")
    body_src = ast.unparse(method)
    assert "has_changed" in body_src, "save should mark app.model.has_changed"


def test_save_handles_missing_app(browsers_ast):
    """The save should wrap the app.model access in try/except so a missing
    app reference doesn't crash."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "save")
    body_src = ast.unparse(method)
    assert "try" in body_src
    assert "except" in body_src


def test_save_returns_snapshot(browsers_ast):
    """The save should return the snapshot dict."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "save")
    body_src = ast.unparse(method)
    assert "return snapshot" in body_src


# ---------- NchantdWebViewer._to_dict ----------

def test_to_dict_returns_snapshot(browsers_ast):
    """``_to_dict`` should return a snapshot dict (not empty)."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "_to_dict")
    assert method is not None
    body_src = ast.unparse(method)
    assert "snapshot" in body_src
    assert "return {}" not in body_src, "_to_dict should not return an empty dict"


def test_to_dict_includes_current_url(browsers_ast):
    """``_to_dict`` should include the current URL."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "_to_dict")
    body_src = ast.unparse(method)
    assert "'current_url'" in body_src or '"current_url"' in body_src


def test_to_dict_includes_title(browsers_ast):
    """``_to_dict`` should include the page title."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "_to_dict")
    body_src = ast.unparse(method)
    assert "'title'" in body_src or '"title"' in body_src


def test_to_dict_safely_reads_browser_title(browsers_ast):
    """``_to_dict`` should wrap the browser.title() call in hasattr/None
    guard so a missing browser doesn't crash."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "_to_dict")
    body_src = ast.unparse(method)
    assert "hasattr" in body_src
    assert "browser.title" in body_src


def test_to_dict_has_docstring(browsers_ast):
    """``_to_dict`` should have a docstring explaining the snapshot fields."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "_to_dict")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "snapshot" in docstring.lower()


# ---------- NchantdCloak stray TODO removal ----------

def test_detect_display_system_no_todo_in_body(apps_ast):
    """The stray TODO in ``_detect_display_system`` body is removed."""
    cls = _find_class(apps_ast, "NchantdCloak")
    if cls is None:
        for node in ast.walk(apps_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "_detect_display_system")
    body_src = ast.unparse(method)
    assert "TODO implement method" not in body_src


def test_detect_display_system_is_intact(apps_source, apps_ast):
    """``_detect_display_system`` should still work after the TODO removal."""
    cls = _find_class(apps_ast, "NchantdCloak")
    if cls is None:
        for node in ast.walk(apps_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "_detect_display_system")
    assert method is not None, "_detect_display_system should still exist"
    body_src = ast.unparse(method)
    # The method should still determine the display system
    assert "_display_system" in body_src


def test_should_use_ozone_is_intact_after_cleanup(apps_source, apps_ast):
    """``_should_use_ozone`` should still be defined after the cleanup."""
    cls = _find_class(apps_ast, "NchantdCloak")
    if cls is None:
        for node in ast.walk(apps_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "_should_use_ozone")
    assert method is not None
    body_src = ast.unparse(method)
    assert "wayland" in body_src
