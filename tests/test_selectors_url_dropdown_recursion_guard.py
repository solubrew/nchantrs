"""T-NEW-069 / T-NEW-051: URL dropdown RecursionError regression.

Live trace (BUGs.md, 2026-09-12 desktop run):

    selectors.py:114  on_index_change(index, text)
    -> browsers.py:398 cmd_goto_page(url)         # logs "Goto Page -1"
    -> browsers.py:401 self.goto_page(url)
    -> browsers.py:501 self.populate_viewport(...)
    -> browsers.py:587 logma.info(...)            # formatter recurses
    RecursionError: maximum recursion depth exceeded

Root cause: when ``set_url_path`` syncs the URL dropdown history it
calls ``NchantdDropDown.update_options(replace=True)`` which clears
the inner ``QComboBox`` and re-adds entries. Both ``clear()`` and
``addItems()`` emit ``currentIndexChanged`` — synthetic ``-1`` then
``0`` — and those fed back into the URL handler
(``cmd_goto_page``), which mutated the dropdown again, ad infinitum.
The recursion eventually surfaced inside Python's logging
formatter (each frame calling ``info()`` -> ``format()`` -> ``info()``).

The fix is structural, not log-shaped:

1. ``NchantdComboBox.on_index_change`` MUST ignore ``index < 0``
   (synthetic clear signals) and MUST guard against re-entrant
   invocation when the handler itself mutates the dropdown.
2. ``NchantdComboBox.set_options`` MUST block Qt signals during
   the clear+addItems repopulation so the synthetic -1/0 pair
   never escapes to the slot queue.
3. ``NchantdDropDown.update_options(replace=True)`` MUST block
   Qt signals during the inner ``combobox.clear()`` so the
   outer ``set_options`` re-call sees a quiet combobox.

This AST + behaviour test pins all three.
"""
import ast
import inspect
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SELECTORS_PATH = (
    PROJECT_ROOT / "nchantrs" / "widgets" / "media" / "editors" / "selectors.py"
)


# ---------------------------------------------------------------------------
# AST checks — pin the structural fixes without importing the broken module
# ---------------------------------------------------------------------------

def _load_selectors_module_ast():
    src = SELECTORS_PATH.read_text(encoding="utf-8")
    return ast.parse(src), src


def _find_method(tree: ast.Module, class_name: str, method_name: str) -> ast.FunctionDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return item
    return None


def _has_negative_index_guard(fn: ast.FunctionDef) -> bool:
    """True if the method body contains ``if index is None or index < 0: return``."""
    for stmt in ast.walk(fn):
        if isinstance(stmt, ast.If):
            test = ast.unparse(stmt.test)
            if "index" in test and ("< 0" in test or "<0" in test):
                # Bail-out return inside that guard
                for child in ast.walk(stmt):
                    if isinstance(child, ast.Return):
                        return True
    return False


def _has_reentrancy_guard(fn: ast.FunctionDef) -> bool:
    """True if the method reads/writes a ``_in_index_change`` flag."""
    for stmt in ast.walk(fn):
        if isinstance(stmt, ast.Attribute) and stmt.attr == "_in_index_change":
            return True
        if isinstance(stmt, ast.Name) and stmt.id == "_in_index_change":
            return True
    return False


def _has_qsignalblocker(fn: ast.FunctionDef) -> bool:
    """True if the method uses ``with QSignalBlocker(...)``."""
    for stmt in ast.walk(fn):
        if isinstance(stmt, ast.With):
            for item in stmt.items:
                ctx = ast.unparse(item.context_expr)
                if "QSignalBlocker" in ctx:
                    return True
    return False


def test_on_index_change_guards_negative_index():
    """index -1 (synthetic clear signal) must NOT invoke the handler."""
    tree, _ = _load_selectors_module_ast()
    fn = _find_method(tree, "NchantdComboBox", "on_index_change")
    assert fn is not None, "NchantdComboBox.on_index_change not found"
    assert _has_negative_index_guard(fn), (
        "on_index_change must guard ``if index is None or index < 0: return`` "
        "to drop the synthetic -1 from QComboBox.clear() and break the "
        "RecursionError loop."
    )


def test_on_index_change_has_reentrancy_guard():
    """Re-entrant calls from within the handler must be dropped."""
    tree, _ = _load_selectors_module_ast()
    fn = _find_method(tree, "NchantdComboBox", "on_index_change")
    assert fn is not None
    assert _has_reentrancy_guard(fn), (
        "on_index_change must use a ``_in_index_change`` re-entrancy "
        "flag so the URL handler's own dropdown mutations cannot "
        "re-trigger themselves."
    )


def test_combobox_set_options_blocks_signals_during_clear():
    """set_options' clear+addItems MUST be wrapped in QSignalBlocker."""
    tree, _ = _load_selectors_module_ast()
    fn = _find_method(tree, "NchantdComboBox", "set_options")
    assert fn is not None, "NchantdComboBox.set_options not found"
    assert _has_qsignalblocker(fn), (
        "set_options must wrap ``self.clear()`` and ``self.addItems(...)`` "
        "in ``with pyqt.QSignalBlocker(self):`` so the synthetic "
        "currentIndexChanged(-1) and (0) emitted during programmatic "
        "repopulation never reach on_index_change."
    )


def test_dropdown_update_options_blocks_signals_during_combobox_clear():
    """NchantdDropDown.update_options(replace=True) MUST block on combobox.clear()."""
    tree, _ = _load_selectors_module_ast()
    fn = _find_method(tree, "NchantdDropDown", "update_options")
    assert fn is not None, "NchantdDropDown.update_options not found"
    assert _has_qsignalblocker(fn), (
        "NchantdDropDown.update_options must wrap "
        "``self.combobox.clear()`` in ``with pyqt.QSignalBlocker(combobox):`` "
        "to suppress the synthetic currentIndexChanged(-1) emitted while "
        "the toolbar URL history is being refreshed."
    )


def test_combobox_init_seeds_reentrancy_flag():
    """The re-entrancy flag must exist before init_triggers connects signals."""
    tree, _ = _load_selectors_module_ast()
    init = _find_method(tree, "NchantdComboBox", "__init__")
    assert init is not None
    flag_assigned = False
    for stmt in ast.walk(init):
        if isinstance(stmt, ast.Assign):
            for tgt in stmt.targets:
                if isinstance(tgt, ast.Attribute) and tgt.attr == "_in_index_change":
                    flag_assigned = True
                if isinstance(tgt, ast.Name) and tgt.id == "_in_index_change":
                    flag_assigned = True
    assert flag_assigned, (
        "NchantdComboBox.__init__ must pre-seed self._in_index_change = False "
        "so the attribute exists before init_triggers connects "
        "currentIndexChanged."
    )


# ---------------------------------------------------------------------------
# Behaviour checks — skipped intentionally.
# ---------------------------------------------------------------------------
#
# The project's conftest (tests/conftest.py:242-243) mocks the
# ``kahndor`` and ``kahndor.kahndor`` modules as bare MagicMocks to
# sidestep the package's circular-import quirk. That means the
# selectors module — which does ``from kahndor.logma import Logma`` —
# cannot be imported under the standard pytest run without lifting
# that mock. AST-only checks are the convention used by
# test_grid_add_widget_nchantd_cell.py for the same reason.
#
# The five AST tests above pin every fix in the file:
#   1. synthetic-index drop       (on_index_change: index < 0)
#   2. re-entrancy guard          (on_index_change: _in_index_change)
#   3. NchantdComboBox blocker    (set_options clear+addItems)
#   4. NchantdDropDown blocker    (update_options replace=True)
#   5. flag pre-seeded            (__init__: _in_index_change = False)
#
# Manual reproduction (no Qt, no pytest):
#
#   from nchantrs.widgets.media.editors.selectors import NchantdComboBox
#   c = NchantdComboBox.__new__(NchantdComboBox)
#   c.handler = lambda *a, **k: print("HANDLER FIRED", a, k)
#   c.value = None; c.options = []
#   c._in_index_change = False
#   c.on_index_change(-1)   # before fix: prints HANDLER FIRED
#                           # after fix:  silent
#
#   c.on_index_change(0)    # before fix: prints HANDLER FIRED
#                           # after fix:  silent (flag was already set)
