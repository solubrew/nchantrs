#!/usr/bin/env python3
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
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from typing import Any
import datetime as dt
from os.path import abspath, dirname, join

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
from nchantrs.widgets.media.editors.editors import NchantdDocEditor, NchantdLabeledEntry
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.wizards.pages import NchantdWizardPage
from nchantrs.wizards.wizards import NchantdWizard
from nchantrs.utilities.users import NchantdUser

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", "users.yaml")


class NchantdNewUserWizard(NchantdWizard):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdNewUserWizard").override(cfg))
        # self.new_application = self.parent.new_application

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        if not self.app.new_application and (self.app.model.is_secure or self.app.model.is_private):
            self.user_name_selector_page = NchantdUserNameSelectorPage().initWidget()
            self.addPage(self.user_name_selector_page)
        cfg = {}
        self.tos_page = NchantdTOSSignOffPage(self, cfg).initWidget()
        self.addPage(self.tos_page)
        self.account_details_page = NchantdNewUserDetailsPage(self, self.config).initWidget()
        self.addPage(self.account_details_page)
        if self.app.new_account and self.app.user.nchantd_account_wizard_visible:
            self.nchantd_account_signup_page = NchantdNewUserSignupPage(self.parent, self.config).initWidget()
            self.addPage(self.nchantd_account_signup_page)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def create_user(self, user=None, user_object=NchantdUser):
        """"""
        user = user_object(self.app, user)
        user.create_user()
        self.app.model.set_user_active(user)


class NchantdTOSSignOffPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdTOSSignOffPage").override(cfg))
        self.document = None
        self.tos_check = None
        logma.info("NchantdTOSSignOffPage initialized")

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """TOSSignOffPage
        2026-09-05
        """
        super().initView()
        text = self.config.dikt["TOS"]
        cfg = {"read-only": True, "text": text}
        self.document = NchantdDocEditor(self, cfg).initWidget()
        self.layout.addWidget(self.document)
        self.registerField("document", self.document)
        self.layout.addSpacing(10)
        cfg = {"text": "by checking this box, I agree to the Terms of Service.", "size": ["auto", "auto"]}
        self.tos_check = NchantdCheckbox(self, cfg).initWidget()
        self.tos_check.setToolTip(cfg["text"])
        self.layout.addWidget(self.tos_check)
        self.registerField("tos_check", self.tos_check)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def validatePage(self) -> bool:
        """Validates that user has manually selected to agree with the TOSSignOffPage
        2026-09-05
        """
        if not self.tos_check.isChecked():
            pyqt.QMessageBox.warning(
                self, "Agreement Required", "You must agree to the terms and conditions to proceed."
            )
            return False
        return True


class NchantdNewUserDetailsPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdFundAccountsTab").override(cfg))
        self.is_app_owner = True
        self.newUser = False
        self.account_nm = None
        self.email = None

    def initModel(self) -> None:
        logma.info("initModel {type(self).__name__}")
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        self.setTitle("New User Account")
        self.setSubTitle("Enter User Details")
        if self.newUser:
            cfg = {"text": "Enter Username:", "layout": "horizontal"}
            self.account_nm = NchantdLabeledEntry(self, cfg).initWidget()
            self.account_nm.setPlaceholderText("Millie Madison")
            self.layout.addWidget(self.account_nm)
            self.registerField("account_nm", self.account_nm)
            cfg = {"text": "Enter Email Address:", "layout": "horizontal"}
            self.email = NchantdLabeledEntry(self, cfg).initWidget()
            self.email.setPlaceholderText("jon.smith@email.com")
            self.layout.addWidget(self.email)
            self.registerField("email", self.email)
        cfg = {
            "text": "Enter Home Location:",
            "layout": "horizontal",
            "Tip": "The more specific the information provided the better the more accurate \n\t\t\t\t\t\tinformation will be provided. Such as weather predictions",
        }
        self.location = NchantdLabeledEntry(self, cfg).initWidget()
        self.location.setPlaceholderText("Zip Code, Area Code, City, State or Address")
        self.layout.addWidget(self.location)
        self.registerField("email", self.location)
        # PUSH TO 0.0.3
        # cfg = {"text": "Select Theme:", "options": ["Blue", "Green", "Red", "Yellow", "Purple", "Pink", "Orange"]}
        # self.color = NchantdRadioButtonGroup(self, cfg).initWidget()
        # self.layout.addWidget(self.color)
        # self.registerField("color", self.color)
        self.new_application = True
        if self.is_app_owner:
            if self.new_application:
                cfg = {"text": "Select Role: ", "options": ["Admin"]}
                self.role = NchantdRadioButtonGroup(self, cfg).initWidget()
                self.layout.addWidget(self.role)
                self.registerField("role", self.role)
            else:
                cfg = {"text": "Select Role: ", "options": ["Admin", "User"]}
                self.role = NchantdRadioButtonGroup(self, cfg).initWidget()
                self.layout.addWidget(self.role)
                self.registerField("role", self.role)
        else:
            cfg = {"text": "Select Role: ", "options": ["User"]}
            self.role = NchantdRadioButtonGroup(self, cfg).initWidget()
            self.layout.addWidget(self.role)
            self.registerField("role", self.role)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdNewUserSignupPage(NchantdWebBrowser):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdNewUserSignupPage").override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdUserNameSelectorPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("NchantdUserNameSelectorPage").override(cfg))
        self.name_selector = None

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = {}
        self.name_selector = NchantdDropDown(self, cfg).initWidget()
        self.layout.addWidget(self.name_selector)
        self.registerField("name_selector", self.name_selector.get_selection)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
