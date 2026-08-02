from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.browsers.browsers import NchantdWebBrowser
from nchantrs.widgets.controls.controls import NchantdRadioButtonGroup
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor
from nchantrs.wizards.pages import NchantdWizardPage
from nchantrs.wizards.wizards import NchantdWizard
from kahndor.logma import Logma
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'accounts.yaml')

class NchantdAddAPIWizard(NchantdWizard):
    """
    1. Ask if user has an API key for the service
    2. if yes provide the entry screen
    3. if no provide a web page to request an apikey for the service
    4. then provide the entry screen to the user
    5. store and verify screen
    6. load account display widget
    """

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdFundAccountsTab')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent)

    def initModel(self) -> None:
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> None:
        logma.info(f'initWidget {{type(self).__name__}}')
        return self

class NchantdNewAccountWizard(NchantdWizard):
    """A Wizard for setting up a new account with a dynamic set of questions that can be provided to the wizard"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdNewAccountWizard')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdNewAccountWizard, self).__init__(self.parent)

    def initModel(self) -> None:
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
        """"""
        self.name_page = NchantdNewAccountNamePage(self, self.config).initWidget()
        self.addPage(self.name_page)

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self