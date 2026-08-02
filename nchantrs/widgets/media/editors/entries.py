from typing import Any
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.editors import NchantdEntryEditor, NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.controls.buttons import NchantdButton
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'entries.yaml')

class NchantdEntryEditorExplainer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdEntryEditorExplainer')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.explainer = None
        logma.info(f'NchantdEntryEditorExplainer initialized')

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = self.config.override({}).dikt
        self.entry = NchantdEntryEditor(self, cfg).initWidget()
        self.layout.addWidget(self.entry)
        self.update_explainer()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def update_explainer(self) -> Any:
        """"""
        if self.explainer is not None:
            self.layout.removeWidget(self.explainer)
            self.explainer.setParent(None)
        self.explainer = NchantdLabel(self, self.config.override({}).dikt).initWidget()
        self.layout.addWidget(self.explainer)
        return self

class NchantdActivateEntry(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """Initialize the view with checkable button via config only"""
        super().initView()
        cfg = self.config.override({'checkable': True}).dikt
        self.enable_button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.enable_button)
        cfg = self.config.override({}).dikt
        self.editor = NchantdEntryBox(self, cfg).initWidget()
        self.layout.addWidget(self.editor)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdCheckboxEditor(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCheckboxEditor'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        cfg = {'layout': 'horizontal'}
        super().initView(cfg)
        cfg = {'text': self.config.dikt.get('label', 'Missing Label'), 'size': self.config.dikt.get('size', ['auto', 'auto'])}
        self.checkbox = NchantdCheckbox(self, cfg).initWidget()
        self.layout.addWidget(self.checkbox)
        cfg = self.config.dikt.get('entrybox')
        cfg['size'] = ['auto', 'auto']
        self.entrybox = NchantdEntryBox(self, cfg).initWidget()
        self.entrybox.setMinimumHeight(30)
        self.layout.addWidget(self.entrybox)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self