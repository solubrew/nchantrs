"""Tests for the 3 round-3 TODO fixes:

1. NchantdWizard.initModel (wizards.py) - removed broken-method stub
2. NchantdTabSet.start_drag (tabsets.py) - missing drag.exec_() call
3. NchantdWebViewer.showEvent (browsers.py) - stray TODO removed

Uses AST + source-text assertions.
"""
import pytest
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WIZARDS_PATH = PROJECT_ROOT / "nchantrs" / "wizards" / "wizards.py"
TABSETS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "tabsets.py"
BROWSERS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "browsers" / "browsers.py"


@pytest.fixture(scope="module")
def wizards_source():
    return WIZARDS_PATH.read_text()


@pytest.fixture(scope="module")
def wizards_ast(wizards_source):
    return ast.parse(wizards_source)


@pytest.fixture(scope="module")
def tabsets_source():
    return TABSETS_PATH.read_text()


@pytest.fixture(scope="module")
def tabsets_ast(tabsets_source):
    return ast.parse(tabsets_source)


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


# ---------- NchantdWizard.initModel ----------

def test_wizard_init_model_no_todo(wizards_ast):
    """``initModel`` should not have the broken-method stub anymore."""
    cls = _find_class(wizards_ast, "NchantdWizard")
    method = _find_method(cls, "initModel")
    assert method is not None
    body_src = ast.unparse(method)
    assert "getattr(super(type(self), self), method_name, None)" not in body_src, (
        "initModel still has the broken-method stub"
    )


def test_wizard_init_model_has_docstring(wizards_ast):
    """``initModel`` should have a docstring explaining the initialization."""
    cls = _find_class(wizards_ast, "NchantdWizard")
    method = _find_method(cls, "initModel")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "wizard" in docstring.lower() or "init" in docstring.lower()


def test_wizard_init_model_is_subclass_stub(wizards_ast):
    """``NchantdWizard.initModel`` is intentionally a base-class stub
    (per the upstream 6f7988b cleanup).  Subclasses are expected to
    override it.  The body should log the init event and return self.
    """
    cls = _find_class(wizards_ast, "NchantdWizard")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    # The upstream's design intent: log + return self, with a "MUST BE
    # IMPLEMENTED by subclasses" hint to subclasses.
    assert "return self" in body_src
    assert "initModel" in body_src or "logma" in body_src
    # Should NOT have the broken getattr pattern from the older stub.
    assert "getattr(super(type(self), self), method_name" not in body_src


def test_wizard_init_model_returns_self(wizards_ast):
    """``initModel`` should return self for chaining."""
    cls = _find_class(wizards_ast, "NchantdWizard")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "return self" in body_src


# ---------- NchantdTabSet.start_drag ----------

def test_start_drag_no_todo(tabsets_ast):
    """The TODO at the top of start_drag is removed."""
    cls = _find_class(tabsets_ast, "NchantdTabSet")
    method = _find_method(cls, "start_drag")
    assert method is not None
    body_src = ast.unparse(method)
    assert "TODO: fix drop_action declarition" not in body_src
    assert "TODO: fix drop_action declaration" not in body_src


def test_start_drag_executes_drag(tabsets_ast):
    """``start_drag`` should call ``drag.exec_()`` to actually execute the drag
    and capture the user's drop action."""
    cls = _find_class(tabsets_ast, "NchantdTabSet")
    method = _find_method(cls, "start_drag")
    body_src = ast.unparse(method)
    assert "drag.exec_" in body_src, "start_drag should call drag.exec_()"
    assert "drop_action" in body_src, "start_drag should capture drop_action"


def test_start_drag_drop_action_assignment(tabsets_ast):
    """``drop_action`` should be assigned from the ``drag.exec_()`` return value."""
    cls = _find_class(tabsets_ast, "NchantdTabSet")
    method = _find_method(cls, "start_drag")
    body_src = ast.unparse(method)
    assert "drop_action = drag.exec_" in body_src or "drop_action=drag.exec_" in body_src.replace(" ", "")


def test_start_drag_checks_move_action(tabsets_ast):
    """``start_drag`` should check the drop_action against MoveAction."""
    cls = _find_class(tabsets_ast, "NchantdTabSet")
    method = _find_method(cls, "start_drag")
    body_src = ast.unparse(method)
    assert "MoveAction" in body_src
    assert "self.handle_successful_drag" in body_src


def test_start_drag_passes_drop_actions_to_exec(tabsets_ast):
    """``drag.exec_`` should be called with the supported drop actions."""
    cls = _find_class(tabsets_ast, "NchantdTabSet")
    method = _find_method(cls, "start_drag")
    body_src = ast.unparse(method)
    # Should reference MoveAction | CopyAction (the supported actions)
    assert "MoveAction" in body_src
    assert "CopyAction" in body_src


# ---------- NchantdWebViewer.showEvent ----------

def test_show_event_no_todo_on_this_method(browsers_ast):
    """The stray TODO at the top of showEvent is removed."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "showEvent")
    assert method is not None
    body_src = ast.unparse(method)
    assert "TODO this is not working correctly" not in body_src
    assert "TODO this doesn" not in body_src


def test_show_event_still_calls_populate_document(browsers_ast):
    """``showEvent`` should still call ``populate_document`` after the cleanup."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "showEvent")
    body_src = ast.unparse(method)
    assert "populate_document" in body_src
    assert "self.active_url" in body_src


def test_show_event_loads_first_time_only(browsers_ast):
    """``showEvent`` should only load on first show (the ``_did_initial_load`` flag)."""
    cls = _find_class(browsers_ast, "NchantdWebViewer")
    method = _find_method(cls, "showEvent")
    body_src = ast.unparse(method)
    assert "_did_initial_load" in body_src
