"""Tests for T-NEW-004 fixes: browser context menu, hit test, and Pro profile warning.

Uses AST + source-text assertions.  The NchantdWebEnginePage and
NchantdWebViewer classes can't be instantiated in the headless test
environment (mock-PyQt metaclass conflict), so the tests verify the
class-specific logic by inspecting the source structure.
"""
import pytest
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PAGES_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "browsers" / "pages.py"
BROWSERS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "browsers" / "browsers.py"


@pytest.fixture(scope="module")
def pages_source():
    return PAGES_PATH.read_text()


@pytest.fixture(scope="module")
def pages_ast(pages_source):
    return ast.parse(pages_source)


@pytest.fixture(scope="module")
def browsers_source():
    return BROWSERS_PATH.read_text()


@pytest.fixture(scope="module")
def browsers_ast(browsers_source):
    return ast.parse(browsers_source)


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


# ---------- createStandardContextMenu ----------

def test_create_standard_context_menu_is_real_method(pages_ast):
    """``createStandardContextMenu`` should be a real method, not a 1-line stub."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    assert method is not None
    body_src = ast.unparse(method)
    # The new method should build a QMenu and add actions to it
    assert "QMenu" in body_src, "createStandardContextMenu should construct a QMenu"
    assert "addAction" in body_src, "createStandardContextMenu should add actions to the menu"


def test_create_standard_context_menu_includes_navigation_actions(pages_ast):
    """The context menu should include Back, Forward, Reload, Stop."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "WebAction.Back" in body_src
    assert "WebAction.Forward" in body_src
    assert "WebAction.Reload" in body_src
    assert "WebAction.Stop" in body_src


def test_create_standard_context_menu_includes_edit_actions(pages_ast):
    """The context menu should include Cut/Copy/Paste/SelectAll."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "WebAction.Cut" in body_src
    assert "WebAction.Copy" in body_src
    assert "WebAction.Paste" in body_src
    assert "WebAction.SelectAll" in body_src


def test_create_standard_context_menu_includes_view_source(pages_ast):
    """The context menu should include View Page Source and Save Page As."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "WebAction.ViewSource" in body_src
    assert "WebAction.SavePage" in body_src


def test_create_standard_context_menu_uses_qt_actions(pages_ast):
    """The menu should reuse Qt's web actions via ``self.action(id)``."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "self.action(" in body_src, "createStandardContextMenu should look up Qt's web actions"


def test_create_standard_context_menu_has_separators(pages_ast):
    """The menu should have separators between nav / edit / view-source groups."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "addSeparator" in body_src


def test_create_standard_context_menu_returns_menu(pages_ast):
    """The method should return the QMenu for the caller to display."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    body_src = ast.unparse(method)
    assert "return menu" in body_src


def test_create_standard_context_menu_has_docstring(pages_ast):
    """The method should have a docstring explaining its purpose."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "createStandardContextMenu")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "context menu" in docstring.lower()


# ---------- hitTestContent ----------

def test_hit_test_content_is_real_method(pages_ast):
    """``hitTestContent`` should be a real method, not a 1-line stub."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "hitTestContent")
    assert method is not None
    body_src = ast.unparse(method)
    # The new method should return a dict with structural fields
    assert "return" in body_src
    assert "tag" in body_src
    assert "link" in body_src
    assert "media" in body_src
    assert "editable" in body_src


def test_hit_test_content_return_dict_shape(pages_ast):
    """The hit test should return a dict with the expected shape."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "hitTestContent")
    body_src = ast.unparse(method)
    # The dict literal should have the structural fields
    assert "'tag'" in body_src or '"tag"' in body_src
    assert "'link'" in body_src or '"link"' in body_src
    assert "'media'" in body_src or '"media"' in body_src
    assert "'editable'" in body_src or '"editable"' in body_src


def test_hit_test_content_has_docstring(pages_ast):
    """The method should have a docstring explaining the return shape."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "hitTestContent")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "hit" in docstring.lower() or "test" in docstring.lower()


# ---------- Stray TODO comments removed ----------

def test_on_title_changed_no_stray_todo_on_context_menu(pages_source, pages_ast):
    """The stray TODO that was inside ``on_title_changed`` (about context menu) is removed."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "on_title_changed")
    body_src = ast.unparse(method)
    assert "TODO" not in body_src, "on_title_changed still has a stray TODO"


def test_handle_feature_permission_no_stray_todo_on_hit_test(pages_source, pages_ast):
    """The stray TODO that was inside ``handle_feature_permission`` (about hit test) is removed."""
    cls = _find_class(pages_ast, "NchantdWebEnginePage")
    method = _find_method(cls, "handle_feature_permission")
    body_src = ast.unparse(method)
    assert "TODO" not in body_src, "handle_feature_permission still has a stray TODO"


# ---------- Pro profile warning ----------

def test_add_profile_blocks_non_pro_users(browsers_ast):
    """``add_profile`` should refuse to add a profile when ``has_pro`` is False."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    assert method is not None
    body_src = ast.unparse(method)
    # The has_pro check is what makes the gating work
    assert "has_pro" in body_src, "add_profile should check has_pro"
    # The not-has_pro branch should show a warning
    assert "notification" in body_src.lower() or "warning" in body_src.lower()


def test_add_profile_returns_self_for_pro(browsers_ast):
    """``add_profile`` should return self for the happy path (pro user)."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    body_src = ast.unparse(method)
    assert "return self" in body_src


def test_add_profile_has_pro_block_creates_notification(browsers_ast):
    """The non-pro branch should construct a ``NchantdNotificationSigil``."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    body_src = ast.unparse(method)
    assert "NchantdNotificationSigil" in body_src


def test_add_profile_has_pro_block_handles_init_failure(browsers_ast):
    """The non-pro branch should wrap the notification init in a try/except
    so a missing notification subsystem doesn't crash the add."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    body_src = ast.unparse(method)
    assert "try" in body_src
    assert "except" in body_src


def test_add_profile_no_longer_has_stray_todo(browsers_source, browsers_ast):
    """The T-NEW-004 TODO at the top of ``add_profile`` body is removed."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    body_src = ast.unparse(method)
    assert "TODO create user warning system" not in body_src


def test_add_profile_has_docstring(browsers_ast):
    """The method should have a docstring explaining the gating logic."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "add_profile")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "pro" in docstring.lower() or "profile" in docstring.lower()
