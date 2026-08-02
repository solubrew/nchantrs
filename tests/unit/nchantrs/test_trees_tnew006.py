"""Tests for T-NEW-006 fixes: treeviews off-by-one, trees read depth,
applicationviews config-TODO cleanup.

Uses AST + source-text assertions.
"""
import pytest
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
TREEVIEWS_PATH = PROJECT_ROOT / "nchantrs" / "views" / "treeviews.py"
TREES_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "trees.py"
APPVIEWS_PATH = PROJECT_ROOT / "nchantrs" / "views" / "applicationviews.py"


@pytest.fixture(scope="module")
def treeviews_source():
    return TREEVIEWS_PATH.read_text()


@pytest.fixture(scope="module")
def treeviews_ast(treeviews_source):
    return ast.parse(treeviews_source)


@pytest.fixture(scope="module")
def trees_source():
    return TREES_PATH.read_text()


@pytest.fixture(scope="module")
def trees_ast(trees_source):
    return ast.parse(trees_source)


@pytest.fixture(scope="module")
def appviews_source():
    return APPVIEWS_PATH.read_text()


@pytest.fixture(scope="module")
def appviews_ast(appviews_source):
    return ast.parse(appviews_source)


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


# ---------- _save_last_node (treeviews.py) ----------

def test_save_last_node_is_real_method(treeviews_ast):
    """``_save_last_node`` should be a real method now (was a stub)."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    assert method is not None
    body_src = ast.unparse(method)
    # Should not be a 1-line return
    assert "return self" in body_src
    assert "logma" in body_src or "warn" in body_src.lower()


def test_save_last_node_persists_to_app_user_state(treeviews_ast):
    """The save should hit the ``app_user_state`` table."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    body_src = ast.unparse(method)
    assert "app_user_state" in body_src, "_save_last_node should write to app_user_state"


def test_save_last_node_uses_node_nid_not_zero(treeviews_ast):
    """The off-by-one fix: the persisted nid should be the actual node's nid,
    not the literal 0 (the previous bug)."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    body_src = ast.unparse(method)
    assert "node.nid" in body_src or "getattr(node" in body_src, (
        "_save_last_node should read nid from the node, not the literal 0"
    )


def test_save_last_node_docstring_documents_off_by_one_fix(treeviews_ast):
    """The docstring should explain the off-by-one fix."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "off-by-one" in docstring.lower() or "nid" in docstring.lower()


def test_save_last_node_uses_parallel_records_columns(treeviews_ast):
    """The save should use the parallel records+columns payload shape."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    body_src = ast.unparse(method)
    assert "'records'" in body_src or '"records"' in body_src
    assert "'columns'" in body_src or '"columns"' in body_src


def test_save_last_node_handles_missing_nid(treeviews_ast):
    """The save should warn (not crash) when the node has no nid."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    body_src = ast.unparse(method)
    assert "warning" in body_src.lower() or "no nid" in body_src.lower()


def test_save_last_node_handles_store_failure(treeviews_ast):
    """The save should wrap the store call in try/except so a missing
    store doesn't crash the navigation."""
    cls = _find_class(treeviews_ast, "NchantdTreeView")
    method = _find_method(cls, "_save_last_node")
    body_src = ast.unparse(method)
    assert "try" in body_src
    assert "except" in body_src


# ---------- add_top_level_items max_depth (trees.py) ----------

def test_add_top_level_items_has_max_depth_parameter(trees_ast):
    """``add_top_level_items`` should accept a ``max_depth`` parameter."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "add_top_level_items")
    assert method is not None
    args = [a.arg for a in method.args.args]
    assert "max_depth" in args, "add_top_level_items should accept max_depth"


def test_add_top_level_items_has_current_depth_parameter(trees_ast):
    """``add_top_level_items`` should track ``current_depth`` for recursion."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "add_top_level_items")
    args = [a.arg for a in method.args.args]
    assert "current_depth" in args


def test_add_top_level_items_respects_max_depth(trees_ast):
    """The method should bail out when ``current_depth >= max_depth``."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "add_top_level_items")
    body_src = ast.unparse(method)
    assert "current_depth >= max_depth" in body_src or "current_depth >= max_depth" in body_src.replace(" ", "")


def test_add_top_level_items_passes_depth_on_recursion(trees_ast):
    """The recursive call should pass ``current_depth + 1``."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "add_top_level_items")
    body_src = ast.unparse(method)
    assert "current_depth + 1" in body_src


def test_add_top_level_items_docstring_documents_max_depth(trees_ast):
    """The docstring should explain the max_depth semantics."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "add_top_level_items")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "max_depth" in docstring or "depth" in docstring.lower()


def test_build_tree_accepts_max_depth(trees_ast):
    """``build_tree`` should accept a ``max_depth`` parameter."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "build_tree")
    args = [a.arg for a in method.args.args]
    assert "max_depth" in args


def test_build_tree_forwards_max_depth(trees_ast):
    """``build_tree`` should forward ``max_depth`` to ``add_top_level_items``."""
    cls = _find_class(trees_ast, "NchantdFileSystem")
    method = _find_method(cls, "build_tree")
    body_src = ast.unparse(method)
    assert "max_depth" in body_src


# ---------- applicationviews.py config TODO cleanup ----------

def test_applicationviews_no_stray_config_todo(appviews_source, appviews_ast):
    """The T-NEW-006 stray TODO + orphan body in applicationviews.py is removed."""
    cls = _find_class(appviews_ast, "NchantdCloakView")
    if cls is None:
        # Try other names
        for candidate in dir(__import__("ast")):
            pass
        # Just check the source
        pass
    assert "TODO we need to make sure the config goes to load Widget" not in appviews_source


def test_on_window_move_method_is_intact(appviews_source, appviews_ast):
    """``on_window_move`` should still exist after the orphan-body cleanup."""
    cls = _find_class(appviews_ast, "NchantdCloakView")
    if cls is None:
        # find any class
        for node in ast.walk(appviews_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "on_window_move")
    assert method is not None, "on_window_move should still exist"
    body_src = ast.unparse(method)
    assert "refresh_window_size" in body_src


def test_refresh_window_size_method_is_intact(appviews_source, appviews_ast):
    """``refresh_window_size`` should still exist after the cleanup."""
    cls = _find_class(appviews_ast, "NchantdCloakView")
    if cls is None:
        for node in ast.walk(appviews_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "refresh_window_size")
    assert method is not None
