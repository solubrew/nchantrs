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

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.checkboxes import NchantdCheckboxGroup, NchantdCheckbox
from nchantrs.widgets.controls.controls import NchantdSelectionWidget
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
from nchantrs.widgets.media.editors.editors import NchantdLabeledEntry
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.panes.panes import NchantdPane
from nchantrs.widgets.controls.button_groups import NchantdAcceptButtons, NchantdFontConfigBar
from ogma.logma import Logma
from subtrix.utilities import uuid

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "catalogs.yaml")


class NchantdNewNodePane(NchantdPane):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdNewNodePane"))
        if parent:
            self.config.override(parent.config)
            self.parent = parent
            self.catalog = self.parent.catalog
        self.config.override(cfg)
        self.config.dikt["action"] = None
        self.active_item = None
        self.select_color = None
        self.select_icon = None
        self.accept_buttons = None
        self.accept_buttons_layout = None
        self.document_type_entry = None
        self.tab_name_entry = None
        self.config_buttons_layout = None
        self.center_layout = None
        self.item_pane_radio_buttons = None
        self.accept_buttons = None
        self.multi_page_import = False
        self.ok = None
        self.open = None
        self.launch_button_layout = None
        self.add_feature = None
        self.node_radio_buttons = None

    def initModel(self):
        """"""
        logma.info(f"Init Model{self.config.dikt.get('action')}")
        self.config.dikt.pop("action")
        super().initModel()
        if self.catalog is None:
            return self
        self.active_item = self.catalog.selected_item
        logma.info(f"Model Initd")
        return self

    def initView(self, cfg=None):
        """"""
        logma.info(f"Init View")
        if cfg is None:
            cfg = {}
        cfg["size"] = ["auto", "auto"]
        super().initView(cfg)
        cfg = {
            "label": "Document Type: ",
            "combobox": {"options": self.config.dikt.get("options", [])},
            "layout": "horizontal",
        }
        self.document_type_entry = NchantdDropDown(self, cfg).initWidget()
        self.left_side_layout.addWidget(self.document_type_entry)
        cfg = {
            "label": "Tab Name: ",
            "layout": "horizontal",
            "value": self.get_new_tab_name(),
            "size": [75, 20],
            "entrybox": {
                "size": [200, 20],
            },
        }
        self.tab_name_entry = NchantdLabeledEntry(self, cfg).initWidget()
        self.left_side_layout.addWidget(self.tab_name_entry)
        self.config_buttons_layout = pyqt.QHBoxLayout()
        cfg = {
            "action": "select_icon",
            "handler": "nchantrs.dialogs.icons.NchantdIconSelectionSigil",
            "size": 48,
            "tip": "Select Icon",
        }
        self.select_icon = NchantdButton(self, cfg).initWidget()  # launch dialog with bit image generator?
        self.config_buttons_layout.addWidget(self.select_icon)
        cfg = {"extend": False, "show_label": False, "highlight": False, "two_rows": False}
        self.font_config = NchantdFontConfigBar(self, cfg).initWidget()
        self.config_buttons_layout.addWidget(self.font_config)
        self.config_buttons_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        self.left_side_layout.addLayout(self.config_buttons_layout)
        self.left_side_layout.addStretch(1)
        self.document_buttons_layout = pyqt.QHBoxLayout()
        self.document_buttons_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop | pyqt.Qt.AlignmentFlag.AlignLeft)
        self.left_side_layout.addLayout(self.document_buttons_layout)
        self.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.center_options_layout = pyqt.QVBoxLayout()
        cfg = {
            "text": "Node Options",
            "description": "",
            "checked": False,
            "multi_options": ["Locked"],
            "size": ["auto", "auto"],
        }
        self.node_checkbox_group = NchantdCheckboxGroup(self, cfg).initWidget()
        self.center_options_layout.addWidget(self.node_checkbox_group)
        self.accept_buttons_layout = pyqt.QHBoxLayout()
        cfg = {"action": None, "handler": self.accept}
        self.accept_buttons = NchantdAcceptButtons(self, cfg).initWidget()
        self.accept_buttons_layout.addWidget(self.accept_buttons)
        self.accept_buttons_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignBottom | pyqt.Qt.AlignmentFlag.AlignRight)
        self.center_layout.addStretch(1)
        self.layout.addLayout(self.accept_buttons_layout)
        self.layout.setSpacing(3)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def accept(self, action=None, app=None, params=None):
        """
        :return:
        """
        super().accept()
        self.add_feature("center")

    def add_field(self, field_widget):
        """"""
        return self

    def add_node(self, tree="left", widgdata=None):
        """"""
        tree = "left"
        if widgdata is None:
            widgdata = {}
        if self.ok:
            name = self.tab_name_entry.textbox.entry_data
            logma.info(f"Active Item {self.active_item.document_nm}")
            if self.active_item.document_nm == "Root Node":
                pid = 0
            elif self.active_item.document_nm in ("Sibling Node", "Child Node"):
                pid = self.app.view.panes[tree].tree.model.current_node.pid
            elif self.active_item.document_nm == "Subtree Node":
                pass
            # has to kick of a much bigger add event
            # self.app.view.panes[tree].model.max_position += 1
            # pos = self.app.view.panes[tree].model.max_position
            pos = 0
            ntype = "usernode"
            tabset = "center"
            parameters = {
                "focus": "user",
                "recent_tab": {
                    # TODO add tab.tid to NchantdDocumentCatalog
                    # "center": self.app.view.panes["center"].model.current_tab.tid,
                    # "right": self.app.view.panes["right"].model.current_tab.tid,
                },
            }
            self.app.model.add_node(name, ntype, pid, pos, parameters, None, True)
        return self

    def get_focus_packages(self):
        """"""
        df = self.app.model.store.get_focus_packages()
        packages = dict(zip(df["sequence_int"].values.list(), df["package_name_txt"].values.list()))
        for key, value in packages.items():
            cfg = {"package_name": value}
            packages[key] = NchantdSelectionWidget(self, cfg)
        return packages

    def get_new_tab_name(self):
        """
        set the name as an document_type and uuid
        :return:
        """
        if self.active_item is None:
            return uuid(5)
        code = self.active_item.title_txt
        if self.active_item.did is None:
            self.active_item.did = uuid()
        name = f"{code[-len(code) + code.rfind("_") + 1 :].lower().replace(' ', '')} {self.active_item.did[-5:]}"
        return name

    def set_active_item(self, item):
        """"""
        self.active_item = item
        return self

    def show_first_tab_options(self):
        """"""
        # [DONE]
        # allow it to be set as a default and then automatically create the tab document with each newly created node
        #

    def update_pane(self):
        """ """
        super().update_pane()
        if self.catalog is not None:
            self.set_active_item(self.catalog.selected_item)
        if self.active_item is not None:
            self.document_type_entry.set_option_selection(self.active_item.title_txt)
            if self.active_item.file_type == "app":
                logma.info(f"Set as Node")
                self.tab_name_entry.set_label("Node Name: ")
                self.add_feature = self.add_node
                if self.node_radio_buttons is not None:
                    self.center_options_layout.removeWidget(self.node_radio_buttons)
                    self.node_radio_buttons.deleteLater()
                    self.node_radio_buttons = None
                # TODO rewrite the left right tab selection
                self.show_first_tab_options()
            elif self.active_item.file_type == "note":
                pass
                # add a floating note  as a feature...store it like a tab but use configurations to put it in sigil ontop of a
                # specific tab at a specific location...have the ability to hide for a period of time...connect to event/task to show back up
                # allow to be assigned to the application/node/tab
            else:
                if self.node_radio_buttons is None:
                    cfg = {"text": "Select Tabset", "layout": "horizontal", "unique_options": ["Center", "Right"]}
                    self.node_radio_buttons = NchantdRadioButtonGroup(self, cfg).initWidget()
                    self.center_options_layout.addWidget(self.node_radio_buttons)
                self.tab_name_entry.set_label("Tab Name: ")
                logma.info(f"Set as Tab")
                self.add_feature = self.add_document
        default_txt = self.get_new_tab_name()
        logma.info(f"Update Default Name {default_txt}")
        # self.tab_name_entry.setPlaceholderText(default_txt)
        self.tab_name_entry.setText(default_txt)
        # self.tab_name_entry.initWidget()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
