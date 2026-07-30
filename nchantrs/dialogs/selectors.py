# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*-
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join

# ======================================3rd Party Library Modules=====================================================||
from typing import Any, Callable, Dict, List, Optional

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidgetMixin
from nchantrs.widgets.widgets import NchantdWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)
if not log:
    logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "selectors.yaml")


class NchantdSelectionDialog(NchantdWidget, pyqt.QDialog):
    """T-NEW-005 (item 3): reusable selection dialog for nchantrs.

    All NchantdDialogs live in the ``nchantrs.dialogs`` package
    per the user's project-wide convention. This dialog shows a
    list of label/callback pairs and lets the user pick one;
    clicking a row runs the callback (which may close the
    dialog or open another widget).

    Acceptance:
        ``NchantdSelectionDialog(title, choices, parent=None)``
        where each choice is a dict with ``"label"`` (str) and
        ``"callback"`` (callable). Returns ``None`` when the user
        cancels.

    Headless behaviour:
        In the absence of an interactive Qt loop
        (``QT_QPA_PLATFORM=offscreen``) the dialog is constructed
        but not shown. The test harness observes the choices via
        ``self.choices``.
    """

    def __init__(self, title=None, choices=None, parent=None, cfg=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title = title or "Select"
        self.choices = list(choices or [])
        self.selected_callback: Optional[Callable[[], Any]] = None
        # KAHNDOR config: best-effort; falls back silently when
        # the yaml file is missing so the dialog still imports
        # cleanly under headless test runners.
        try:
            self.config = kahndor.Instruct(pxcfg).select(
                "NchantdSelectionDialog"
            )
            if parent is not None and hasattr(parent, "config"):
                self.config = self.config.override(parent.config)
            if cfg is not None:
                self.config = self.config.override(cfg)
        except Exception as exc:
            logma.warning(
                f"[selectors] NchantdSelectionDialog: kahndor "
                f"config fallback — {exc}"
            )
            self.config = kahndor.Instruct({})
        self.initModel()
        self.initView()
        self.initWidget()

    def initModel(self, cfg=None) -> None:
        """Initialise the model layer (T-NEW-005 item 3).

        Validates that every choice has a ``label`` (str) and a
        ``callback`` (callable). Filters out malformed entries
        with a warning rather than raising — the dialog still
        opens for the valid rows.
        """
        valid = []
        for entry in self.choices:
            if not isinstance(entry, dict):
                logma.warning(
                    "[selectors] NchantdSelectionDialog: skipping "
                    "non-dict choice "
                    f"{entry!r}"
                )
                continue
            label = entry.get("label")
            callback = entry.get("callback")
            if not isinstance(label, str) or not callback:
                logma.warning(
                    "[selectors] NchantdSelectionDialog: skipping "
                    "choice missing label/callback "
                    f"{entry!r}"
                )
                continue
            valid.append({"label": label, "callback": callback})
        self.choices = valid
        return self

    def initView(self, cfg=None) -> None:
        """Build the dialog window (T-NEW-005 item 3).

        A vertical layout with a label (the title) and a list
        widget showing every choice. Double-clicking a row runs
        the callback and closes the dialog.
        """
        self.setWindowTitle(self.title)
        layout = pyqt.QVBoxLayout()
        title_label = pyqt.QLabel(self.title)
        layout.addWidget(title_label)
        self.list_widget = pyqt.QListWidget()
        for entry in self.choices:
            item = pyqt.QListWidgetItem(entry["label"])
            # Stash the callback on the item for run_callback().
            item.setData(pyqt.Qt.UserRole, entry["callback"])
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)
        # OK / Cancel buttons.
        button_box = pyqt.QDialogButtonBox(
            pyqt.QDialogButtonBox.Ok | pyqt.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        # Double-click on a row also triggers the callback.
        self.list_widget.itemDoubleClicked.connect(self.run_callback)
        self.setLayout(layout)
        self.setGeometry(300, 300, 500, 400)
        return self

    def initWidget(self) -> None:
        """Hook any final widget bindings (T-NEW-005 item 3)."""
        return self

    def run_callback(self, item=None) -> None:
        """Run the selected row's callback and close the dialog.

        The test harness observes ``self.selected_callback`` so it
        can assert on the chosen row without needing a real mouse
        click. In production this is wired to ``itemDoubleClicked``
        and the OK button.
        """
        callback = None
        if item is not None:
            callback = item.data(pyqt.Qt.UserRole)
        elif self.list_widget is not None and self.list_widget.currentItem() is not None:
            current = self.list_widget.currentItem()
            callback = current.data(pyqt.Qt.UserRole)
        self.selected_callback = callback
        if callable(callback):
            try:
                callback()
            except Exception as exc:
                logma.error(
                    f"[selectors] NchantdSelectionDialog callback failed: {exc}",
                    exc_info=True,
                )
        # Headless / non-modal: don't call accept() because Qt
        # may segfault when accepting a dialog that was never
        # exec()'d. The test harness observes
        # ``self.selected_callback`` to confirm the choice.
        try:
            if self.isVisible():
                self.accept()
        except Exception:
            pass
        return self

    def exec(self) -> int:
        """Run the dialog modally; ``1`` = accepted, ``0`` = rejected.

        Subclasses ``QDialog.exec`` so ``QInputDialog``-style
        usage (``dlg.exec()`` / ``dlg.selected_callback``) works
        for headless tests that can't drive a real mouse click.
        """
        # In the headless env (QT_QPA_PLATFORM=offscreen) the
        # dialog can't actually show; tests bypass this via
        # ``selected_callback`` and ``choices``.
        return super().exec()
