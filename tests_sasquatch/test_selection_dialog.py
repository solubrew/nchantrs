"""T-NEW-005 (item 3) UI: NchantdSelectionDialog regression test.

Per user direction (2026-07-29): all NchantdDialogs live in the
``nchantrs.dialogs`` package. The selection dialog takes a list
of ``{label, callback}`` choices and runs the chosen callback
when the user clicks OK (or double-clicks a row).

Test surface:
  1. Imports cleanly (no circular imports with the rest of
     nchantrs).
  2. Constructor accepts ``title``, ``choices``, ``parent``.
  3. ``initModel`` filters malformed choices (no label, no
     callback, non-dict entries).
  4. ``run_callback`` runs the chosen callback and sets
     ``selected_callback`` for headless test assertions.
"""

import os

import pytest
from PySide6 import QtWidgets

# Headless Qt platform is required for the dialog to construct
# without a display server.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="session")
def qapp():
    """Provide a single QApplication for the entire test session.

    Required by NchantdSelectionDialog — QWidget subclasses can't
    construct without an active QApplication. The instance is
    reused across tests via the session scope.
    """
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    yield app


def test_imports_cleanly():
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    assert NchantdSelectionDialog is not None


def test_constructor_accepts_title_choices_parent(qapp):
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    callback_calls = []
    choices = [
        {"label": "alpha", "callback": lambda: callback_calls.append("alpha")},
        {"label": "beta", "callback": lambda: callback_calls.append("beta")},
    ]
    dlg = NchantdSelectionDialog(
        title="Browse Instances",
        choices=choices,
        parent=None,
    )
    assert dlg.title == "Browse Instances"
    assert len(dlg.choices) == 2
    # Window title shows the user-supplied title.
    assert dlg.windowTitle() == "Browse Instances"


def test_init_model_filters_malformed_choices(qapp):
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    valid_calls = []
    choices = [
        # Valid entry.
        {"label": "alpha", "callback": lambda: valid_calls.append("alpha")},
        # Non-dict entry — skipped.
        "bad entry",
        # Dict without label — skipped.
        {"callback": lambda: valid_calls.append("nope")},
        # Dict without callback — skipped.
        {"label": "missing cb"},
        # Valid entry.
        {"label": "beta", "callback": lambda: valid_calls.append("beta")},
    ]
    dlg = NchantdSelectionDialog(title="Test", choices=choices)
    assert len(dlg.choices) == 2
    labels = [c["label"] for c in dlg.choices]
    assert labels == ["alpha", "beta"]


def test_run_callback_invokes_chosen_callback(qapp):
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    calls = []
    choices = [
        {"label": "first", "callback": lambda: calls.append("first")},
        {"label": "second", "callback": lambda: calls.append("second")},
    ]
    dlg = NchantdSelectionDialog(title="Test", choices=choices)
    # Simulate the user picking the second row by setting
    # currentItem() to row 1 and invoking run_callback(None).
    if dlg.list_widget.count() >= 2:
        dlg.list_widget.setCurrentRow(1)
    dlg.run_callback(None)
    assert calls == ["second"]
    # The selected_callback attribute records the choice.
    assert dlg.selected_callback is not None


def test_run_callback_handles_missing_callback_gracefully(qapp):
    """Defence: a choice with a None callback should not crash."""
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    choices = [{"label": "noop", "callback": None}]
    dlg = NchantdSelectionDialog(title="Test", choices=choices)
    # initModel filters out the None-callback entry.
    assert dlg.choices == []


def test_dialog_has_list_widget_with_one_row_per_choice(qapp):
    from nchantrs.dialogs.selectors import NchantdSelectionDialog

    choices = [
        {"label": "row-1", "callback": lambda: None},
        {"label": "row-2", "callback": lambda: None},
        {"label": "row-3", "callback": lambda: None},
    ]
    dlg = NchantdSelectionDialog(title="Test", choices=choices)
    assert dlg.list_widget.count() == 3
    assert dlg.list_widget.item(0).text() == "row-1"
    assert dlg.list_widget.item(2).text() == "row-3"
