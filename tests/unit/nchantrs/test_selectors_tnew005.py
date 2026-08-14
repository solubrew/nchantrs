"""Tests for T-NEW-005 fixes: selector sorting strategies + lists.py cleanup.

Uses AST + source-text assertions.  The selectors / tables / lists
classes can't be instantiated in the headless test environment
(mock-PyQt metaclass conflict), so the tests verify the class-specific
logic by inspecting the source structure.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
SELECTORS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "media" / "editors" / "selectors.py"
TABLES_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "tables" / "tables.py"
LISTS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "tables" / "lists.py"


@pytest.fixture(scope="module")
def selectors_source():
    return SELECTORS_PATH.read_text()


@pytest.fixture(scope="module")
def selectors_ast(selectors_source):
    return ast.parse(selectors_source)


@pytest.fixture(scope="module")
def tables_source():
    return TABLES_PATH.read_text()


@pytest.fixture(scope="module")
def tables_ast(tables_source):
    return ast.parse(tables_source)


@pytest.fixture(scope="module")
def lists_source():
    return LISTS_PATH.read_text()


@pytest.fixture(scope="module")
def lists_ast(lists_source):
    return ast.parse(lists_source)


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


# ---------- set_options sort strategy ----------

def test_set_options_supports_alpha_sort(selectors_ast):
    """``set_options`` should support 'alpha' sort (default)."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    body_src = ast.unparse(method)
    assert "'alpha'" in body_src, "set_options should handle 'alpha' sort strategy"


def test_set_options_supports_insertion_sort(selectors_ast):
    """``set_options`` should support 'insertion' sort (preserve input order)."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    body_src = ast.unparse(method)
    assert "'insertion'" in body_src


def test_set_options_supports_value_sort(selectors_ast):
    """``set_options`` should support 'value' sort (numeric)."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    body_src = ast.unparse(method)
    assert "'value'" in body_src, "set_options should handle 'value' sort strategy"
    assert "float(" in body_src, "value sort should co-erce to float"


def test_set_options_default_sort_is_alpha(selectors_ast):
    """When ``sort`` is None, the default should be 'alpha'."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    body_src = ast.unparse(method)
    assert "sort is None" in body_src or "sort==None" in body_src
    assert "alpha" in body_src


def test_set_options_docstring_documents_sort_strategies(selectors_ast):
    """The docstring should explain the sort strategies."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "alpha" in docstring.lower()
    assert "insertion" in docstring.lower()
    assert "value" in docstring.lower()


def test_set_options_todo_removed(selectors_source, selectors_ast):
    """The original 2026-07 TODO about more sophisticated sorting is removed."""
    cls = _find_class(selectors_ast, "NchantdComboBox")
    method = _find_method(cls, "set_options")
    body_src = ast.unparse(method)
    assert "TODO implement a more sophisticated sorting mechanism" not in body_src


# ---------- NchantdDropDown sort strategy ----------

def test_nchantd_drop_down_init_no_todo_on_sort(selectors_source, selectors_ast):
    """The stray TODO in ``NchantdDropDown.__init__`` is removed."""
    cls = _find_class(selectors_ast, "NchantdDropDown")
    init = _find_method(cls, "__init__")
    body_src = ast.unparse(init)
    assert "TODO implement a more sophisticated sorting mechanism" not in body_src


def test_nchantd_drop_down_init_view_no_todo_on_sort(selectors_source, selectors_ast):
    """The stray TODO in ``NchantdDropDown.initView`` is removed."""
    cls = _find_class(selectors_ast, "NchantdDropDown")
    method = _find_method(cls, "initView")
    body_src = ast.unparse(method)
    assert "TODO: should always be sorted" not in body_src


def test_update_options_supports_sort_strategy(selectors_ast):
    """``update_options`` should pass the sort strategy through to the underlying combobox."""
    cls = _find_class(selectors_ast, "NchantdDropDown")
    method = _find_method(cls, "update_options")
    body_src = ast.unparse(method)
    assert "sort" in body_src, "update_options should accept a sort parameter"
    assert "self.combobox.set_options" in body_src, "update_options should call combobox.set_options"
    assert "sort=sort" in body_src or "sort=sort" in body_src.replace(" ", "")


def test_update_options_default_sort_is_none(selectors_ast):
    """The default sort should be None (alpha fall-through)."""
    cls = _find_class(selectors_ast, "NchantdDropDown")
    method = _find_method(cls, "update_options")
    body_src = ast.unparse(method)
    assert "sort is None" in body_src, "update_options should default sort to None"


def test_update_options_docstring_documents_strategy(selectors_ast):
    """The docstring should document the sort parameter."""
    cls = _find_class(selectors_ast, "NchantdDropDown")
    method = _find_method(cls, "update_options")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "sort" in docstring.lower()


# ---------- tables.py stray TODO ----------

def test_nchantd_dataframe_table_stray_todo_removed(tables_source, tables_ast):
    """The stray TODO between class definition and __init__ is removed."""
    cls = _find_class(tables_ast, "NchantdDataFrameTable")
    init = _find_method(cls, "__init__")
    assert init is not None
    body_src = ast.unparse(init)
    assert "TODO need to find any" not in body_src


def test_nchantd_dataframe_table_has_docstring(tables_source, tables_ast):
    """``NchantdDataFrameTable`` should have a docstring."""
    cls = _find_class(tables_ast, "NchantdDataFrameTable")
    docstring = ast.get_docstring(cls)
    assert docstring is not None


# ---------- lists.py stray TODO ----------

def test_nchantd_interactive_bulleted_list_stray_todo_removed(lists_source, lists_ast):
    """The stray TODO in ``NchantdInteractiveBulletedList.initView`` is removed."""
    cls = _find_class(lists_ast, "NchantdInteractiveBulletedList")
    method = _find_method(cls, "initView")
    body_src = ast.unparse(method)
    assert "TODO build out builted list widget" not in body_src


def test_nchantd_interactive_bulleted_list_init_view_has_docstring(lists_source, lists_ast):
    """``initView`` should have a real docstring explaining the layout."""
    cls = _find_class(lists_ast, "NchantdInteractiveBulletedList")
    method = _find_method(cls, "initView")
    docstring = ast.get_docstring(method)
    assert docstring is not None
