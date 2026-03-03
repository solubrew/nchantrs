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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.utilities.utils import convert_df_to_tree, lookup
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "menus.yaml")
pxcfg = {}


class NchantdMenu(pyqt.QMenu):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdMenu")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.actions = None
        self.menus = {}

    def initModel(self):
        """ """
        # need to lookup the action
        self.actions = self.config.dikt.get("actions", [])
        return self

    def initView(self):
        """ """
        for action in self.actions:
            logma.info(f"Action {action}")
            self.add_action(action["name_txt"], action["handler"])
        return self

    def initWidget(self):
        """ """
        return self

    def add_action(self, title, handler):
        """"""
        action = pyqt.QAction(title, self)
        if handler is not None and handler != "":
            handler = getattr(self.parent, handler)
            action.triggered.connect(handler)
        self.addAction(action)
        return self

    def buildMenu(self, menu=None, menus=None):
        """Build menu from menu configuration tree"""
        if menus is None:
            return self
        for code, subcode in menus.items():  # ||Menubar Code
            logma.info(f"Code {code} Subcode {subcode}")
            logma.info(f"Menus {self.menus}")
            # menu_cfg = lookup(self.parent.app, code, None, True, True, False)
            menu_cfg = self.menu_df[self.menu_df["name_txt"] == code].to_dict("records")[0]
            logma.info(f"Menu {menu_cfg}")
            if menu_cfg["name_txt"] is None:
                menu_cfg["name_txt"] = code
            if menu not in self.menus:
                self.menus[menu] = self.addMenu(f"{menu_cfg['name_txt']}")
            self.menus[code] = self.menus[menu].addMenu(f"{menu_cfg['name_txt']}")
            # self.menus[code] = self.addMenu(f"{menu_cfg['name_txt']}")
            if subcode is not None and not subcode == {}:
                self.buildMenu(code, subcode)
            else:
                logma.info(f"Action {menu_cfg['name_txt']} {menu_cfg['handler']}")
                if menu_cfg["handler"] is None or menu_cfg["handler"] == "":
                    continue
                if hasattr(self.parent, menu_cfg.get("handler", None)):
                    self.add_action(menu_cfg["name_txt"], getattr(self.parent, menu_cfg["handler"]))
        return self


class NchantdContextMenu(NchantdMenu):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdContextMenu"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.menu_data = None
        self.name = None

    def initModel(self):
        """"""
        super().initModel()
        self.name = self.config.dikt.get("name", None)
        return self

    def initView(self):
        """"""
        super().initView()
        self.buildMenu(self.name, self.menu_data)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def get_menu(self, name=None):
        """"""
        logma.info(f"Name {name}")
        if name:
            self.name = name
        # self.menu_df = self.parent.app.model.get_menu(self.name)
        logma.info(f"Menu Data {self.menu_df.head()}")
        menu_data = convert_df_to_tree(self.menu_df)
        logma.info(f"Menu Data {menu_data}")
        if self.menu_data is None:
            self.menu_data = menu_data
        else:
            self.menu_data.update(menu_data)
        logma.info(f"Menu Data {self.menu_data.keys()}")
        self.buildMenu(self.name, self.menu_data)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
