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
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.selectors import NchantdDropDown
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from nchantrs.widgets.media.editors.editors import NchantdDocEditor, NchantdLabeledEntry
from nchantrs.wizards.pages import NchantdWizardPage
from nchantrs.wizards.wizards import NchantdWizard
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "users.yaml")


class NchantdNewUserWizard(NchantdWizard):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdNewUserWizard"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app = self.parent.app
        self.new_application = self.parent.new_application

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()

        if not self.app.new_application and (self.app.model.is_secure or self.app.model.is_private):
            # only password protected will get the opportutnity to select otherwise its all handled in the background
            self.user_name_selector_page = NchantdUserNameSelectorPage().initWidget()
            # allow for selection of user name but without password this could be poor UX
            self.addPage(self.user_name_selector_page)

        cfg = {}
        self.tos_page = NchantdTOSSignOffPage(self, cfg).initWidget()
        # store to app_collection and send to telemetry service
        self.addPage(self.tos_page)

        self.account_details_page = NchantdNewUserDetailsPage(self, self.config).initWidget()
        self.addPage(self.account_details_page)

        if self.app.new_account and self.app.user.nchantrs_account_wizard_visible:
            # White Labeled System Accounts will have one automatically mostly outside the users perview
            self.nchantrs_account_signup_page = NchantdNewUserSignupPage(self.parent, self.config).initWidget()
            self.addPage(self.nchantrs_account_signup_page)
        # self.currentIdChanged.connect(self.on_next_clicked)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdTOSSignOffPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdTOSSignOffPage"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.document = None
        self.tos_check = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
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

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def validatePage(self):
        """"""
        if not self.tos_check.isChecked():
            # Show a warning message to the user
            pyqt.QMessageBox.warning(
                self,
                "Agreement Required",
                "You must agree to the terms and conditions to proceed.",
            )
            return False  # Prevent the wizard from moving forward
        # If the checkbox is checked, allow moving to the next page
        return True


class NchantdNewUserDetailsPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFundAccountsTab")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdNewUserDetailsPage, self).__init__(self.parent, self.config)
        self.is_app_owner = True
        self.app = self.parent.app
        self.newUser = False

    def initModel(self):
        """"""

    def initView(self):
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
            "Tip": """The more specific the information provided the better the more accurate 
						information will be provided. Such as weather predictions""",
        }
        self.location = NchantdLabeledEntry(self, cfg).initWidget()
        self.location.setPlaceholderText("Zip Code, Area Code, City, State or Address")
        self.layout.addWidget(self.location)
        self.registerField("email", self.location)

        cfg = {
            "text": "Select Theme:",
            "options": [
                "Blue",
                "Green",
                "Red",
                "Yellow",
                "Purple",
                "Pink",
                "Orange",
            ],
        }
        self.color = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.color)
        self.registerField("color", self.color)

        # TODO PRO: implement once Pro level software is ready
        # cfg = {'text': 'Select Security Level', 'options': ['Medium', 'High']}
        # self.security_level = NchantdRadioButtonGroup(self, cfg).initWidget()
        # self.layout.addWidget(self.security_level)
        # self.registerField('security_level', self.security_level)
        #
        # cfg = {'text': 'Select Privacy Level', 'options': ['Medium', 'High']}
        # self.security_level = NchantdRadioButtonGroup(self, cfg).initWidget()
        # self.layout.addWidget(self.security_level)
        # self.registerField('privacy_level', self.security_level)

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

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdNewUserSignupPage(NchantdWebBrowser):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdNewUserSignupPage")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdNewUserSignupPage, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdUserNameSelectorPage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdUserNameSelectorPage")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdUserNameSelectorPage, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()

        cfg = {}
        self.name_selector = NchantdDropDown(self, cfg).initWidget()
        self.layout.addWidget(self.name_selector)
        self.registerField("name_selector", self.name_selector)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
