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
from condor import condor

import logging
from nchantrs.libraries import pyqt

logger = logging.getLogger(__name__)
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.advanced_buttons import NchantdLabeledDoubleSpinBox, NchantdLabeledSpinBox
from nchantrs.widgets.controls.button_groups import NchantdAcceptButtons
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.widgets.media.editors.selectors import NchantdDropDown, NchantdComboBox
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.tables.lists import NchantdList
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.groups import NchantdGridScrollGroupBox, NchantdVScrollGroupBox, NchantdHScrollGroupBox
from nchantrs.widgets.groups import NchantdHGroupBox, NchantdGroup
from nchantrs.widgets.config.config import NchantdConfigStoreDocument
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "settings.yaml")


class NchantdSettingsWidget(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdSettingsWidget")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.unsaved = False
        self.document = NchantdConfigStoreDocument()

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        cfg = {"layout": "horizontal", "justify": "right", "size": ["auto", 50]}
        buttons = {
            0: {"action": "show_pane_left", "handler": self.cmd_show_pane_left},
            49: "_stretch",
            100: {"action": "save", "handler": self.cmd_save},
            1000: {"action": "show_pane_right", "handler": self.cmd_show_pane_right},
        }
        self.button_bar = NchantdButtonBar(self, cfg).initWidget(buttons)
        self.button_bar.setFixedHeight(36)
        self.layout.addWidget(self.button_bar)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_export_file(self):
        """"""

    def cmd_import_file(self):
        """"""

    def cmd_save(self):
        """"""

    def cmd_show_pane_left(self, event=None, *args, **kwargs):
        """"""
        # TODO flip icon
        if self.app.view.panes["left"].isHidden():
            self.app.view.panes["left"].show()
        else:
            self.app.view.panes["left"].hide()
        return self

    def cmd_show_pane_right(self, event=None, *args, **kwargs):
        """"""
        # TODO flip icon
        if self.app.view.panes["right"].isHidden():
            self.app.view.panes["right"].show()
        else:
            self.app.view.panes["right"].hide()
        return self

    def export_settings(self):
        """"""
        # launch a file selection sigil

    def get_settings(self, area):
        """"""
        df = self.app.model.get_settings(area)
        return df

    def import_settings(self):
        """"""
        # launch a file selection sigil

    def launch_unsaved_dialog(self):
        """"""
        # launch a sigil that forces the user to decide on saving or not

    def on_changed(self, value):
        """"""
        self.unsaved = True

    def onFocusOut(self):
        """"""
        super().onFocusOut()
        if self.unsaved:
            self.launch_unsaved_dialog()
            self.unsaved = False

    def save(self):
        """"""
        self.on_widget_changed()

    def set_defaults(self):
        """"""
        for setting in self.setting_configs:
            self.app.model.store_setting(setting)


class NchantdInterfaceSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdInterfaceSettingsTab"))
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdThemeSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(condor.Instruct(pxcfg).select("NchantdThemeSettingsTab"))
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        self._load_themes()

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        self.config.dikt.pop("height", None)
        self.config.dikt.pop("width", None)
        # logma.info(f"Themes {self.themes}")
        darks = [x for x in self.themes.keys() if "midnight" in x]
        lights = [x for x in self.themes.keys() if "midday" in x]
        if len(self.themes.keys()) != 0:
            # logma.info(f"Load Dark Themes{darks}")
            cfg = {"size": ["auto", "auto"]}
            dark_group = pyqt.QGroupBox()
            dark_group.setTitle("Themes")
            dark_group_layout = pyqt.QVBoxLayout()
            for theme in darks:
                if self.themes[theme]["active"]:
                    # logma.info(f"Theme {theme}")
                    # theme_group = NchantdHGroupBox(self, self.config).initWidget()
                    cfg = {"size": ["auto", "auto"]}
                    theme_group = pyqt.QGroupBox()
                    theme_group.setTitle(self.themes[theme]["name"])
                    theme_group_layout = pyqt.QHBoxLayout()
                    theme_group.setLayout(theme_group_layout)
                    cfg = {"text": "Set Active"}
                    button = NchantdButton(self, cfg).initWidget()
                    theme_group_layout.addWidget(button)
                    color = self.themes[theme]["palette"]["primary"]["accent"]
                    cfg = {"text": self.themes[theme]["name"], "color": color, "size": [150, 100]}
                    label = NchantdLabel(self, cfg).initWidget()
                    theme_group_layout.addWidget(label)
                    cfg = {"color": self.themes[theme]["palette"]["primary"]["accent"], "size": [400, 100]}
                    image = NchantdImage(self, cfg).initWidget()
                    # image.setFixedSize(400, 100)
                    theme_group.setSizePolicy(
                        pyqt.QSizePolicy.Policy.MinimumExpanding, pyqt.QSizePolicy.Policy.MinimumExpanding
                    )
                    theme_group_layout.addWidget(image)
                    dark_group_layout.addWidget(theme_group)
                    # theme_group.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft)
            self.layout.addLayout(dark_group_layout)
            self.setSizePolicy(pyqt.QSizePolicy.Policy.Minimum, pyqt.QSizePolicy.Policy.Minimum)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def save(self):
        """"""
        super().save()
        return self

    def _load_themes(self):
        """"""
        self.themes = self.app.view.themes
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
