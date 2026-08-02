from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets import controls
from kahndor.logma import Logma
from nchantrs.widgets.controls.radios import NchantdRadioButtonGroup
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', '.yaml')

class NchantdWizardPage(pyqt.QWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdFundAccountsTab')
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app = self.parent.app

    def initModel(self) -> None:
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> Any:
        """
        A stackable page of widgets with a bottom configured navigation buttons

        """
        self.layout = pyqt.QVBoxLayout()
        self.setLayout(self.layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdSelectInstancePage(NchantdWizardPage):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdSelectInstancePage')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self.parent)
        self.config.override(cfg)
        self.app = self.parent.app

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        if self.app.recent_documents:
            cfg = {'text': 'Select Recent Document', 'options': self.parent.recent_documents}
            self.select_document = NchantdRadioButtonGroup(self, cfg)
            self.layout.addWidget(self.select_document)
            self.registerField('select_document', self.select_document)
        cfg = {'text': 'Select Area of Focus:', 'options': {'Finance': ['Personal Budgeting', 'Business Accounting', 'Investing'], 'Task Management': [], 'Graphic Design': []}}
        self.checks = NchantdRadioButtonGroup(self, cfg).initWidget()
        self.layout.addWidget(self.checks)
        self.registerField('focus_check', self.checks)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self