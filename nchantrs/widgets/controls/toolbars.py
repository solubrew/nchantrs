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
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.media.editors.editors import NchantdEntryBox, NchantdEntryEditor
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.widgets import NchantdWidget
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "toolbars.yaml")


class NchantdButtonBar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdButtonBar").override(cfg))
        self.buttons = {}
        self.actions = {}
        self.layout = None

    def initModel(self, actions=None):
        """"""
        super().initModel()
        if actions is None:
            actions = self.config.dikt.get("actions", None)
        if actions is not None:
            self.set_actions(actions)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        logma.info(f"Action Items {self.actions}")
        for action, button_cfg in self.actions.items():
            if isinstance(action, int):
                sequence = action
            if isinstance(button_cfg, str):
                action = button_cfg
                if button_cfg[0] == "_":  # implement an internal triger
                    if button_cfg == "_insert_stretch":
                        self.layout.addStretch()
                    elif button_cfg == "_insert_spacer":
                        self.layout.addSpacerItem(
                            pyqt.QSpacerItem(20, 40, pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Minimum)
                        )
                    elif button_cfg == "_insert_separator":
                        self.layout.addSeparator()
                    elif button_cfg == "_skip":
                        pass
                    continue
            elif isinstance(button_cfg, dict):
                action = button_cfg.get("action", button_cfg.get("name", None))
            if action is None:
                continue
            self.buttons[action] = {}
            action_cfg = kahndor.Instruct(lookup(self.app, action)).override(self.config)
            if isinstance(button_cfg, dict):
                action_cfg.override(button_cfg)
            self.buttons[action]["widget"] = action_cfg.dikt.get("widget", None)
            if isinstance(self.buttons[action]["widget"], str):
                self.buttons[action]["widget"] = None
            logma.info(f"Action Config {action_cfg.dikt.get("buttons", None)}")
            if self.buttons[action].get("widget", None) is None:
                if action_cfg.dikt.get("type", None) == "dropdown":
                    self.buttons[action]["widget"] = NchantdDropDown(self, action_cfg)
                elif action_cfg.dikt.get("type", None) == "entry":
                    self.buttons[action]["widget"] = NchantdEntryBox(self, action_cfg)
                elif action_cfg.dikt.get("type", None) == "entry_editor":
                    self.buttons[action]["widget"] = NchantdEntryEditor(self, action_cfg)
                else:
                    self.buttons[action]["widget"] = NchantdButton(self, action_cfg)
            logma.info(f"Action Widget Configuration {action} {self.buttons[action]['widget']}")
            self.buttons[action]["widget"].initWidget()
            self.layout.addWidget(self.buttons[action]["widget"])

            self.buttons[action]["widget"].layout.setContentsMargins(0, 0, 0, 0)
            self.buttons[action]["widget"].layout.setSpacing(3)
        if self.config.dikt.get("justify", None) is None:
            self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft | pyqt.Qt.AlignmentFlag.AlignTop)
        else:
            self._set_alignment()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(3)
        self.setSizePolicy(pyqt.QSizePolicy.Policy.MinimumExpanding, pyqt.QSizePolicy.Policy.MinimumExpanding)
        return self

    def initWidget(self, buttons=None):
        """"""
        self.initModel(buttons)
        self.initView()
        return self

    def set_actions(self, actions=None):
        """"""
        if actions is None:
            actions = self.config.dikt.get("actions", {})
        self.actions = actions
        return self

    def switch_to_toggle(self):
        """
        switch all buttons to toggle type
        allow for a block on buttons that is defined specifically
        :return:
        """
        for action, button_data in self.buttons.items():
            if button_data.get("block_toggle", False):
                continue
            else:
                widget = button_data.get("widget", None)
                if widget and hasattr(widget, "setCheckable"):
                    # Check if not already initialized with checkable via config
                    cfg = widget.config.dikt if hasattr(widget, "config") else {}
                    if not cfg.get("checkable", False):
                        widget.setCheckable(True)


class NchantdMenuBar(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdMenuBar")
        if parent:
            self.config.override(parent.config)
        super().__init__(self.parent)
        self.config.override(cfg)
        self.menus = {}

    def buildMenu(self, menubar=None, menus=None):
        """Build menu from menu configuration tree"""
        if log:
            logma.info(f"Menus {menus}")
        if isinstance(menus, dict):
            for menu in menus.keys():
                if log:
                    logma.info(f"Menu {menu}")
                menu_data = self.menus_data[self.menus_data["name_txt"] == menu]
                menu_cfg = {}
                if menu_data["is_action_bit"].values.tolist()[0] == 1:
                    menu_cfg = lookup(self.parent.parent, menu)
                menu_ = menubar.addMenu(menu_cfg["name_txt"] if menu_cfg.get("name_txt", None) else menu)
                if menus[menu] is not None:
                    self.buildMenu(menu_, menus[menu])
        return self

    def initModel(self):
        """ """
        self.menus_data = self.app.model.store.get_app_menu()
        return self

    def initView(self):
        """ """
        self.mainMenu = self.app.main.menuBar()
        # self.mainMenu.setNativeMenuBar(True)
        if log:
            logma.info(f"Menus Data {self.menus_data}")
        tree = convert_df_to_tree(self.menus_data, "0", {})
        if log:
            logma.info(f"Menus Tree {tree}")
        self.buildMenu(self.mainMenu, tree)
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self


class NchantdToolBar(pyqt.QToolBar):
    """Standard Nchantd Toolbar"""

    def __init__(self, parent, cfg: dict = None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdToolBar")
        self.config.override(cfg)
        super().__init__()
        self.app = pyqt.QApplication.instance()
        self.actions = {}
        self.set_actions()

        logma.info(f"Tool Bar Parent {self.parent}")
        self.theme = None
        self.toolbar = pyqt.QToolBar()

    def buildToolbar(self):
        """Build toolbar from toolbar configuration tree"""
        self.toolbar.setMovable(True)
        self.toolbar.setFloatable(True)
        if self.config.dikt.get("layout", None) == "horizontal":
            self.toolbar.setOrientation(pyqt.Qt.Horizontal)
        else:
            self.toolbar.setOrientation(pyqt.Qt.Vertical)
        for seq, code in self.actions.items():
            action = lookup(self.app, code)
            name = action["name_txt"]
            btn = pyqt.QToolButton()
            if action.get("icon_txt", None):
                btn.setIcon(pyqt.QIcon(self.theme.get_icon_path(action["icon_txt"], "base")))
            else:
                btn.setText(name)
            if action.get("tip_txt", None):
                btn.setToolTip(action.get("tip_txt"))
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.toolbar.addWidget(btn)
        return self.toolbar

    def initModel(self, actions=None):
        """"""
        if actions is not None:
            self.set_actions(actions)
        return self

    def initView(self, cfg=None):
        """ """
        self.config.override(cfg)
        self.theme = self.app.view.theme
        self.app.main.addToolBar(self.buildToolbar())
        # if self.actions:
        # 	for action in self.actions:
        # 		path = self.theme.get_icon_path(action, 'base')
        # 		logma.info(f"ToolBar Action Path {path}")
        # 		if path is not None:
        # 			action_W = pyqt.QAction(pyqt.QIcon(path))
        # 			self.addAction(action_W)
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self

    def set_actions(self, actions=None):
        """"""

        logma.info(f"Toolbar Config {self.config.dikt.keys()}")
        self.actions = self.config.dikt.get("actions", {})

        logma.info(f"Actions {self.actions}")
        return self


class NchantdApplicationToolBar(NchantdToolBar):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        super().__init__(self.parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdApplicationToolBar"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()

        logma.info(f"Toolbar Config {self.config.dikt.keys()}")
        cfg = {
            "layout": "horizontal",
            "text": "Search",
            "default": ["Tree", "Internet", "Local Filesystem", "Cloud Filesystem"],
        }
        search_dropdown = NchantdDropDown(self, cfg).initWidget()
        self.toolbar.addWidget(search_dropdown)
        search_entry = NchantdEntryBox(self, self.config).initWidget()
        self.toolbar.addWidget(search_entry)
        action = lookup(self.app, "search_go")
        # cfg = {action}
        #search_button = NchantdButton(self, action).initWidget()
        #self.toolbar.addWidget(search_button)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdRecordNavigationToolbar(NchantdToolBar):
    """Standard Nchantd Record Navigation Toolbar"""

    def __init__(self, cfg: dict = {}):
        """ """
        self.config = kahndor.Instruct(pxcfg)
        self.config.select("nchantdrecordnavigationtoolbar").override(cfg)
        super(NchantdRecordNavigationToolbar, self).__init__()
        self.model = NchantdTableModel(app, self.config.dikt, parent)
        self.layout = pyqt.QHBoxLayout()
        self.config.dikt["text"] = "Backward"
        self.backBTN = NchantdToolButton(self, self.config.dikt["text"])
        self.backBTN.clicked.connect(self.prevRecord())
        self.layout.addWidget(self.backBTN)
        self.config.dikt["Label"] = "Go To:"
        self.gotoLineEditor = NchantdLineEditor()
        self.layout.addWidget(self.gotoLineEditor)
        self.goBTN = NchantdButton()
        self.goBTN.clicked.connect(self.findRecord())
        self.layout.addWidget(self.goBTN)
        self.config.dikt["text"] = "Forward"
        self.foreBTN = NchantdToolButton(self, self.config.dikt["text"])
        self.foreBTN.clicked.connect(self.nextRecord)
        self.layout.addWidget(self.foreBTN)
        self.setLayout(self.layout)

    def nextRecord(self):
        """ """
        return self

    def prevRecord(self):
        """ """
        return self

    def findRecord(self):
        """ """
        return self


class NchantdSettingsToolBar(NchantdToolBar):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdSettingsToolBar")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()

        logma.info(f"Toolbar Config {self.config.dikt.keys()}")
        cfg = {
            "layout": "horizontal",
            "text": "Search",
            "default": ["Tree", "Internet", "Local Filesystem", "Cloud Filesystem"],
        }
        search_dropdown = NchantdDropDown(self, cfg).initWidget()
        self.toolbar.addWidget(search_dropdown)
        search_entry = NchantdEntryBox(self, self.config).initWidget()
        self.toolbar.addWidget(search_entry)
        action = lookup(self.app, "search_go")
        # cfg = {action}
        search_button = NchantdButton(self, action).initWidget()
        self.toolbar.addWidget(search_button)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
