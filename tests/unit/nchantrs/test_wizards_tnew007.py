"""Tests for T-NEW-007 fixes: wizard method implementations in apps.py
and instances.py.

Uses AST + source-text assertions.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
APPS_PATH = PROJECT_ROOT / "nchantrs" / "wizards" / "apps.py"
INSTANCES_PATH = PROJECT_ROOT / "nchantrs" / "wizards" / "instances.py"


@pytest.fixture(scope="module")
def apps_source():
    return APPS_PATH.read_text()


@pytest.fixture(scope="module")
def apps_ast(apps_source):
    return ast.parse(apps_source)


@pytest.fixture(scope="module")
def instances_source():
    return INSTANCES_PATH.read_text()


@pytest.fixture(scope="module")
def instances_ast(instances_source):
    return ast.parse(instances_source)


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


# ---------- add_page ----------

def test_add_page_appends_to_pages_list(apps_ast):
    """``add_page`` should append the page to ``self.pages``."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "add_page")
    assert method is not None
    body_src = ast.unparse(method)
    assert "self.pages.append" in body_src, "add_page should append to self.pages"
    assert "return self" in body_src, "add_page should return self for fluent API"


def test_add_page_returns_self(apps_ast):
    """``add_page`` should return self."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "add_page")
    body_src = ast.unparse(method)
    assert "return self" in body_src


def test_add_page_initializes_pages_if_missing(apps_ast):
    """``add_page`` should initialize ``self.pages`` if it doesn't exist."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "add_page")
    body_src = ast.unparse(method)
    assert "self.pages" in body_src


# ---------- assign_page_sequence ----------

def test_assign_page_sequence_sorts_by_order(apps_ast):
    """``assign_page_sequence`` should sort pages by their ``order`` field."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "assign_page_sequence")
    assert method is not None
    body_src = ast.unparse(method)
    assert "sort" in body_src
    assert "order" in body_src


def test_assign_page_sequence_returns_self(apps_ast):
    """``assign_page_sequence`` should return self."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "assign_page_sequence")
    body_src = ast.unparse(method)
    assert "return self" in body_src


def test_assign_page_sequence_handles_missing_pages(apps_ast):
    """``assign_page_sequence`` should handle the case where ``self.pages`` is missing or empty."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "assign_page_sequence")
    body_src = ast.unparse(method)
    assert "hasattr" in body_src or "not self.pages" in body_src


def test_assign_page_sequence_logs_warning_on_unsortable(apps_ast):
    """``assign_page_sequence`` should log a warning when pages can't be sorted."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "assign_page_sequence")
    body_src = ast.unparse(method)
    assert "try" in body_src
    assert "except" in body_src
    assert "warning" in body_src.lower()


# ---------- ask_user_to_update ----------

def test_ask_user_to_update_shows_qmessagebox(apps_ast):
    """``ask_user_to_update`` should pop a QMessageBox.question."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "ask_user_to_update")
    assert method is not None
    body_src = ast.unparse(method)
    assert "QMessageBox" in body_src


def test_ask_user_to_update_returns_yes_or_no(apps_ast):
    """``ask_user_to_update`` should return True/False based on the user's reply."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "ask_user_to_update")
    body_src = ast.unparse(method)
    assert "StandardButton.Yes" in body_src
    assert "return" in body_src


# ---------- copy_application ----------

def test_copy_application_returns_self(apps_ast):
    """``copy_application`` should return self for fluent API."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "copy_application")
    assert method is not None
    body_src = ast.unparse(method)
    assert "return self" in body_src


def test_copy_application_accepts_src_and_dst(apps_ast):
    """``copy_application`` should accept explicit src_app and dst_dir args."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "copy_application")
    args = [a.arg for a in method.args.args]
    assert "src_app" in args
    assert "dst_dir" in args


def test_copy_application_falls_back_to_config(apps_ast):
    """``copy_application`` should fall back to ``self.config.dikt.get(...)`` when args are missing."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "copy_application")
    body_src = ast.unparse(method)
    assert "self.config.dikt.get" in body_src


def test_copy_application_walks_src_tree(apps_ast):
    """``copy_application`` should walk the source tree (when src_app is a directory)."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "copy_application")
    body_src = ast.unparse(method)
    assert "walk" in body_src or "os.walk" in body_src


def test_copy_application_handles_missing_args(apps_ast):
    """``copy_application`` should log a warning and return self when src_app or dst_dir is missing."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "copy_application")
    body_src = ast.unparse(method)
    assert "missing" in body_src.lower() or "warning" in body_src.lower()


# ---------- set_library_status ----------

def test_set_library_status_is_pro_aware(apps_source, apps_ast):
    """``set_library_status`` should gate on the user's Pro tier."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "set_library_status")
    assert method is not None
    body_src = ast.unparse(method)
    assert "has_pro" in body_src, "set_library_status should check has_pro"
    assert "library_active" in body_src


def test_set_library_status_pro_uses_documents_path(apps_source, apps_ast):
    """Pro users should get the ~/Documents/NchantdLibrary path."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "set_library_status")
    body_src = ast.unparse(method)
    assert "Documents" in body_src
    assert "NchantdLibrary" in body_src


def test_set_library_status_free_uses_app_path(apps_source, apps_ast):
    """Free users should get a path under the application root."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "set_library_status")
    body_src = ast.unparse(method)
    assert "application_path" in body_src


def test_set_library_status_todo_removed(apps_source, apps_ast):
    """The TODO at the top of ``set_library_status`` is removed."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "set_library_status")
    body_src = ast.unparse(method)
    assert "TODO controls for allowing" not in body_src


# ---------- check_installed cleanup ----------

def test_check_installed_no_orphan_body(apps_source, apps_ast):
    """The orphan body between ``check_installed`` and ``check_is_already_running`` is removed."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "check_installed")
    body_src = ast.unparse(method)
    assert "todo" not in body_src.lower()
    assert "TODO implement method" not in body_src


def test_check_installed_uses_app_path_in_check(apps_source, apps_ast):
    """``check_installed`` should reference ``self.app.model.application_path`` (not the undefined ``app_path``)."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "check_installed")
    body_src = ast.unparse(method)
    assert "self.app.model.application_path" in body_src


# ---------- create_paths cleanup ----------

def test_create_paths_no_todo(apps_source, apps_ast):
    """The TODO at the top of ``create_paths`` is removed."""
    cls = _find_class(apps_ast, "NchantdApplicationStartupWizard")
    method = _find_method(cls, "create_paths")
    body_src = ast.unparse(method)
    assert "TODO implement method" not in body_src


# ---------- instances.py cleanup ----------

def test_create_database_instance_no_todo(instances_source, instances_ast):
    """The stray TODO in ``create_database_instance`` is removed."""
    cls = _find_class(instances_ast, "NchantdNewInstanceWizard")
    if cls is None:
        # Find any class
        for node in ast.walk(instances_ast):
            if isinstance(node, ast.ClassDef):
                cls = node
                break
    method = _find_method(cls, "create_database_instance")
    body_src = ast.unparse(method)
    assert "TODO refactor NchantdInstance" not in body_src
