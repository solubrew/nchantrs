from typing import Any

from os.path import abspath, dirname, join
import datetime as dt
import logging

logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from nchantrs.widgets.media.editors.editors import NchantdDocEditor, NchantdLabeledEntry
from nchantrs.wizards.pages import NchantdWizardPage
from nchantrs.wizards.wizards import NchantdWizard
from kahndor.logma import Logma

here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, "_data_", "users.yaml")


class NchantdNewUserWizard(NchantdWizard):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdNewUserWizard").override(cfg))
        self.app = self.parent.app
        self.new_application = self.parent.new_application

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
        if self.app.new_account and self.app.user.nchantrs_account_wizard_visible:
            self.nchantrs_account_signup_page = NchantdNewUserSignupPage(self.parent, self.config).initWidget()
            self.addPage(self.nchantrs_account_signup_page)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTOSSignOffPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTOSSignOffPage"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.document = None
        self.tos_check = None
        logma.info(f"NchantdTOSSignOffPage initialized")

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
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
        """"""
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
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdFundAccountsTab")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdNewUserDetailsPage, self).__init__(self.parent, self.config)
        self.is_app_owner = True
        self.app = self.parent.app
        self.newUser = False

    def initModel(self) -> None:
        logma.info(f"initModel {{type(self).__name__}}")
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
        cfg = {"text": "Select Theme:", "options": ["Blue", "Green", "Red", "Yellow", "Purple", "Pink", "Orange"]}
        self.color = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.color)
        self.registerField("color", self.color)
        if self.is_app_owner:
            if self.parent.new_application:
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

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdNewUserSignupPage(NchantdWebBrowser):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdNewUserSignupPage")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdNewUserSignupPage, self).__init__(self.parent, self.config)

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
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdUserNameSelectorPage")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdUserNameSelectorPage, self).__init__(self.parent, self.config)

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
        self.registerField("name_selector", self.name_selector)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self
