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
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.groups import NchantdVScrollGroupBox, NchantdHGroupBox, NchantdGridScrollGroupBox
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.config.settings import NchantdSettingsWidget

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "packages.yaml")
pxcfg = {}


class NchantdPackageSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdPackageSettings")
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        super().__init__(parent, self.config)
        self.levels = self.config.dikt.get("levels", [])
        self.primary_settings_group = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        self.primary_settings_group = NchantdGridScrollGroupBox()
        self.primary_settings_group.scroll.setHorizontalScrollBarPolicy(pyqt.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.primary_settings_group.setTitle("Package Settings")
        self.packages = {}
        packages = self.config.dikt.get("packages", {})
        split_lock = False
        cnt = 0
        packages = {key: packages[key] for key in sorted(packages)}
        for package in sorted(packages, key=lambda x: packages[x]["requires_pro"]):
            if self.app.model.user.has_pro is False and packages[package]["requires_pro"] is True:
                if split_lock is False:
                    split_lock = True
                    cfg = {"text": "Get Pro Edition", "size": [100, 30], "justify": "center"}
                    self.primary_settings_group.addWidget(NchantdButton(self, cfg).initWidget(), cnt, 0)
                    cnt += 1
            package_group = pyqt.QGroupBox()
            package_group.setTitle(package)
            package_layout = pyqt.QGridLayout()
            package_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
            package_group.setLayout(package_layout)
            self.primary_settings_group.addWidget(package_group, cnt, 0)
            if package not in self.packages.keys():
                self.packages[package] = {}
            cfg = {"text": f"Enable {package}", "layout": "horizontal", "size": ["auto", 30]}
            self.packages[package]["enable"] = NchantdCheckbox(self, cfg).initWidget()
            package_layout.addWidget(self.packages[package]["enable"], 0, 0)
            cfg = {"text": f"Insert {package} Focus", "layout": "horizontal", "size": ["auto", 30]}
            self.packages[package]["focus"] = NchantdCheckbox(self, cfg).initWidget()
            package_layout.addWidget(self.packages[package]["focus"], 0, 1)
            themes = self.config.dikt.get("themes", [])
            cfg = {
                "label": f"Select Theme for Focus: ",
                "layout": "horizontal",
                "combobox": {"options": themes},
                "size": ["auto", 30],
            }
            self.packages[package]["theme"] = NchantdDropDown(self, cfg).initWidget()
            package_layout.addWidget(self.packages[package]["theme"], 0, 2)
            if self.app.model.user.has_pro is False and packages[package]["requires_pro"] is True:
                self.packages[package]["enable"].setDisabled(True)
                self.packages[package]["focus"].setDisabled(True)
                self.packages[package]["theme"].setDisabled(True)
            package_group.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
            cnt += 1

        self.primary_settings_group.layout.setAlignment(
            pyqt.Qt.AlignmentFlag.AlignCenter | pyqt.Qt.AlignmentFlag.AlignTop
        )
        self.layout.addLayout(self.primary_settings_group.layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def get_settings(self):
        """"""
        return super().get_settings("packages")

    def save(self):
        """"""
        super().save()
        for package in self.packages:
            if self.packages[package]["enable"].changed:
                if self.packages[package]["enable"].isChecked():
                    if self.packages[package]["focus"].isChecked():
                        theme = self.packages[package]["theme"].currentText()
                        self.app.model.store.insert_focus(package, theme)

        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
