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
from os.path import dirname, join
from kahndor import kahndor
from typing import Optional, Dict, List, Any, Tuple
import logging
logger = logging.getLogger(__name__)
from nchantrs.dialogs.dialogs import NchantdSigil, NchantdErrorNotifySigil
from nchantrs.libraries import pyqt
from nchantrs.widgets.media.editors.editors import NchantdLabeledEntry
from nchantrs.widgets.controls.buttons import NchantdTabSideButtons
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', 'new.yaml')

class NewNchantdAPIKeyManualEntrySigil(NchantdSigil):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdNewAPIKeyManualEntry').override(cfg))

    def initModel(self) -> None:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initModel {{type(self).__name__}}')
        return self

    def initView(self) -> None:
        """

        show link to sigup for service

        show link to request/setup page for apikeys

        where to launch the links when clicked?

        :return:
        """
        cfg = {'text': 'Enter API Key: '}
        self.api_key_entry = NchantdLabeledEntry(self, cfg).initWidget()
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self

class NewNchantdNodeSigil(NchantdSigil):
    """"""

    def __init__(self, parent=None, nid='0', cfg=None) -> None:
        """ """
        super().__init__('node', parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NewNchantdNodeSigil').override(cfg))
        self.nid = nid
        self.name = None
        self.icon = None
        self.buttons = None

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        self.hide_title()
        cfg = {'text': 'Enter Node Name: '}
        self.name = NchantdLabeledEntry(self, cfg).initWidget()
        self.add_field(self.name)
        cfg = {'text': 'Select Node Icon: '}
        self.icon = NchantdLabeledEntry(self, cfg).initWidget()
        self.add_field(self.icon)
        self.add_accept_buttons()
        return self

class NewNchantdTabSigil(NchantdSigil):
    """"""

    def __init__(self, name='tab', parent=None, cfg=None) -> None:
        """ """
        super().__init__(name, parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NewNchantdTabSigil').override(cfg))
        self.name = None
        self.icon = None
        self.buttons = None

    def finalizeView(self, cfg=None) -> None:
        """"""
        self.add_accept_buttons(cfg)
        return self

    def initModel(self) -> None:
        """"""
        super().initModel()
        return self

    def initView(self) -> None:
        """"""
        super().initView()
        self.hide_title()
        layout = pyqt.QHBoxLayout()
        logma.info(f'Config {self.config.dikt.keys()}')
        cfg = {'text': 'Enter Tab Name:', 'default_text': f"{self.config.dikt['default_text']} {self.config.dikt['short_name']}"}
        self.name = NchantdLabeledEntry(self, self.config.override(cfg)).initWidget()
        layout.addWidget(self.name)
        buttons = NchantdTabSideButtons().initWidget()
        layout.addWidget(buttons)
        self.layout.addLayout(layout)
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        self.finalizeView()
        self.run()
        return self

    def validate(self) -> None:
        """"""
        super().validate()
        if self.name.textbox.text() in ('', None):
            cfg = {'text': 'No Value Provided for Node Entry Name'}
            NchantdErrorNotifySigil('error_notify', self, cfg).initWidget()
            self.reject()
            return None