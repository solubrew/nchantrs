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
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.config.settings import NchantdSettingsWidget
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.groups import NchantdVScrollGroupBox, NchantdGroup
from kahndor.logma import Logma
from pycurity.pyvalid import validate_password_strength, validate_pin

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "security.yaml")


class NchantdSecuritySettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSecuritySettingsTab"))
        self.parent = parent
        if self.parent is not None:
            self.config.override(self.parent.config)
        self.config.override(cfg)
        self.levels = self.config.dikt.get("levels", [])
        self.primary_settings_group = None
        self.button_bar = None
        self.user_group = None
        self.current_user = None
        self.select_user = None
        self.allow_share_local_user = None
        self.allow_share_remote_user = None
        self.password_group = None
        self.old_password = None
        self.new_password = None

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        if cfg is None:
            cfg = {}
        cfg["size"] = ["auto", "auto"]
        super().initView(cfg)
        # cfg = {"layout": "horizontal", "justify": "right"}
        # buttons = {0: "import_file", 1: "export_document", 2: "save"}
        # self.button_bar = NchantdButtonBar(self, cfg).initWidget(buttons)
        # self.layout.addWidget(self.button_bar)
        self.primary_settings_group = NchantdVScrollGroupBox(self, cfg)
        self.primary_settings_group.setTitle("Security Settings")
        cfg = {"size": ["auto", "auto"]}
        self.user_group = pyqt.QGroupBox(self, cfg)
        self.user_group.setTitle("Users")
        user_layout = pyqt.QGridLayout()
        user_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        self.user_group.setLayout(user_layout)
        self.primary_settings_group.addWidget(self.user_group)

        user = "solubrew"[DONE]
        cfg = {"label": f"Current User: {user}", "layout": "horizontal", "size": ["auto", "auto"]}
        self.current_user = NchantdLabel(self, cfg).initWidget()
        user_layout.addWidget(self.current_user, 0, 0)

        options = [user, "New User"]
        cfg = {
            "label": f"Available Users:",
            "layout": "horizontal",
            "combobox": {"options": options, "size": ["auto", "auto"]},
            "handler": self.cmd_on_change_user_select,
        }
        self.select_user = NchantdDropDown(self, cfg).initWidget()
        user_layout.addWidget(self.select_user, 1, 0, 1, 2)

        user_layout.setColumnStretch(2, 0)

        # PUSH:
        # cfg = {"text": "Allow Sharing Between Local Users", "layout": "horizontal"}
        # self.allow_share_local_user = NchantdCheckbox(self, cfg).initWidget()
        # user_layout.addWidget(self.allow_share_local_user, 0, 3)
        # cfg = {"text": "Allow Sharing Between Remote Users", "layout": "horizontal"}
        # self.allow_share_remote_user = NchantdCheckbox(self, cfg).initWidget()
        # user_layout.addWidget(self.allow_share_remote_user, 1, 3)
        cfg = {}
        self.password_group = pyqt.QGroupBox()
        self.password_group.setTitle("Password")
        password_layout = pyqt.QGridLayout()
        password_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        password_layout.setSpacing(3)
        self.password_group.setLayout(password_layout)
        self.primary_settings_group.addWidget(self.password_group)

        # if old user password was not autogenered
        cfg = {
            "label": "Enter Old Local User Password",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "handler": self.cmd_on_old_password_edit,
        }
        self.old_password = NchantdEntryEditor(self, cfg).initWidget()
        password_layout.addWidget(self.old_password, 0, 0)

        cfg = {
            "label": "Enter New Local User Password",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "handler": self.cmd_on_new_password_edit,
        }
        self.new_password = NchantdEntryEditor(self, cfg).initWidget()
        password_layout.addWidget(self.new_password, 1, 0)

        cfg = {
            "label": "Confirm New Local User Password",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "handler": self.cmd_on_new_password_cofirm_edit,
        }
        self.confirmed_new_password = NchantdEntryEditor(self, cfg).initWidget()
        password_layout.addWidget(self.confirmed_new_password, 2, 0)

        cfg = {
            "text": "Enable Lock Screen",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "handler": self.cmd_on_change_enable_lock_screen,
        }
        self.lock_switch = NchantdCheckbox(self, cfg).initWidget()
        password_layout.addWidget(self.lock_switch, 0, 1)

        options = [1, 3, 5, 15, 30, 45, 60, 120]
        cfg = {
            "label": "Lock Screen Time Out (Mins): ",
            "layout": "horizontal",
            "combobox": {"options": options},
            "size": ["auto", "auto"],
            "handler": self.cmd_on_change_lock_screen_timeout,
        }
        self.lock_screen_timeout = NchantdDropDown(self, cfg).initWidget()
        password_layout.addWidget(self.lock_screen_timeout, 1, 1)

        cfg = {
            "text": "Enable Lock Screen Pin",
            "layout": "horizontal",
            "size": ["auto", "auto"],
            "handler": self.cmd_on_change_enable_lock_screen_pin,
        }
        self.enable_lock_switch = NchantdCheckbox(self, cfg).initWidget()
        password_layout.addWidget(self.enable_lock_switch, 2, 1)

        cfg = {
            "label": "Lock Screen Pin Entry",
            "layout": "horizontal",
            "entrybox": {"size": [100, "auto"]},
            "size": ["auto", "auto"],
            "handler": self.cmd_on_change_lock_screen_pin_edit,
        }
        self.lock_screen_pin = NchantdEntryEditor(self, cfg).initWidget()
        password_layout.addWidget(self.lock_screen_pin, 3, 1)

        # PUSH
        # self.encryption_group = NchantdGroup()
        # self.encryption_group.setTitle("Encryption")
        # encryption_group_layout = pyqt.QGridLayout()
        # encryption_group_layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        # self.encryption_group.setLayout(encryption_group_layout)
        # self.primary_settings_group.addWidget(self.encryption_group)
        #
        # cfg = {"label": "Reset Encryption", "layout": "horizontal"}
        # self.encryption_reset = NchantdEntryEditor(self, cfg).initWidget()
        # encryption_group_layout.addWidget(self.encryption_reset, 0, 0)

        self.layout.addLayout(self.primary_settings_group.layout)
        self.set_size()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_on_change_user_select(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_change_enable_lock_screen(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_change_enable_lock_screen_pin(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_change_lock_screen_timeout(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_change_lock_screen_pin_edit(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_old_password_edit(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_new_password_edit(self, event=None, *args, **kwargs):
        """"""
        return self

    def cmd_on_new_password_cofirm_edit(self, event=None, *args, **kwargs):
        """"""
        return self

    def get_settings(self):
        """"""
        return super().get_settings("security")

    def save(self):
        """"""
        super().save()
        if self.old_password is not None:
            if self.current_user != "New User":
                if self._verify_password(self.old_password):
                    if self._validate_password(self.old_password, self.new_password, self.confirmed_new_password):
                        self.app.model.user.change_password(self.current_user, self.new_password)
        if self.enable_lock_switch.changed:
            lock_out_mins = self.lock_screen_timeout.value
            if self.enable_lock_screen_pin.isChecked():
                pin = self.lock_screen_pin.value
                self.app.model.user.enable_lock_screen(self.current_user, lock_out_mins, pin)
        return self

    def _validate_password(self, old, new, connew):
        """"""
        if new != old:
            if validate_password_strength(new)["valid"]:
                if new == connew:
                    return True
        return False

    def _validate_pin(self, pin):
        """"""

    def _verify_password(self, old):
        """"""

    def _verify_pin(self, pin):
        """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
