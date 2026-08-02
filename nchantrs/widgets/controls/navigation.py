from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', '.yaml')

class NchantdNavigationButtons(pyqt.QWidget):
    """ """

    def __init__(self, parent=None, cfg={}) -> None:
        """ """
        self.config = kahndor.Instruct(pxcfg).override(cfg)
        self.config.select('NchantdNavigationButtons')
        if parent:
            self.config.override(parent.config)
        self.parent = parent
        pyqt.QWidget.__init__(self)
        self.layout = pyqt.QHBoxLayout()
        if log:
            logma.info(f'Nchantd Submission Buttons {self.config.dikt}')
        self.config.dikt['buttons']['next']['text'] = 'Next'
        self.prevbutton = NchantdButton(self, self.config.dikt['buttons']['prev'])
        self.prevbutton.initWidget()
        self.layout.addWidget(self.prevbutton)
        self.config.dikt['buttons']['jump']['input'] = ''
        self.jumpinput = editors.NchantdEntryEditor(self, self.config.dikt['buttons']['input'])
        self.jumpinput.initWidget()
        self.layout.addWidget(self.jumpinput)
        self.config.dikt['buttons']['jump']['text'] = 'Jump'
        self.jumpbutton = NchantdButton(self, self.config.dikt['buttons']['jump'])
        self.jumpbutton.initWidget()
        self.layout.addWidget(self.jumpbutton)
        self.config.dikt['buttons']['prev']['text'] = 'Prev'
        self.nextbutton = NchantdButton(self, self.config.dikt['buttons']['next'])
        self.nextbutton.initWidget()
        self.layout.addWidget(self.nextbutton)
        self.setLayout(self.layout)

    def initWidget(self) -> Any:
        super().initWidget()
        logma.info(f'initWidget {{type(self).__name__}}')
        return self