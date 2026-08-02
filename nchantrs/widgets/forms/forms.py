from typing import Any
"#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>: #\t\t\t\t\t\t\t\t||\n        DOCid: 'b0383757-eb6b-4d01-a5af-f0b4bc6b3b44' #\t\t\t\t\t\t\t\t||\n        name: Nchantrs Module Widgets Forms Python Excecution Document  #\t\t\t||\n        description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        version: <[version]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n"
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from nchantrs.libraries import pyqt
logger = logging.getLogger(__name__)
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.widgets import loadWidget
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(abspath(here), '_data_', 'forms.yaml')

class NchantdForm(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdForm'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdDynamicEntryForm(NchantdForm):
    """A single pane widget for building a simple top down entry form with a
    submission button at the end of the form"""

    def __init__(self, parent=None, cfg={}) -> None:
        """

        :param parent:
        :param cfg:
        """
        super().__init__(parent, cfg)
        logma.info(f'Init NchantdDynamicEntryForm Config {cfg}')
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdDynamicEntryForm').override(cfg))
        self.fieldWDGTs = {}
        self.controlWDGTs = {}
        self.handlers = {}

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel()
        for control in self.config.dikt.get('controls', {}).keys():
            handler = self.config.dikt['controls'].get(control, {}).get('handler', 'default')
            self.handlers[control] = getattr(self, handler)
        self.values = {}
        self.handlers = {}
        self.rid = None
        return self

    def initView(self) -> Any:
        """The pane is built with fields not sure how to abstract this

        TODO: need to get max columns grid in order to span other fields
        """
        super().initView({'layout': 'grid'})
        x, y = (0, 0)
        y = self._build_controls(y, x)
        y += 1
        self._build_fields(y)
        return self

    def initWidget(self) -> Any:
        """ """
        self.reset = None
        self.initModel(self.reset)
        self.initView()
        return self

    def add_entry(self) -> Any:
        """ """
        self.rid = self.app.model.store.add(self.values)
        return self

    def delete_entry(self, record) -> Any:
        """ """
        self.model.deleteRecord(record)
        return self

    def jump_entry(self, record) -> Any:
        """ """
        self.model.getRecord(record)
        return self

    def next_entry(self) -> None:
        """ """
        self.rid = self.app.model.store.next(self.rid)

    def previous_entry(self) -> None:
        """ """
        self.rid = self.app.model.store.prev(self.rid)

    def cancel_entry(self) -> None:
        """ """
        self.rid = None

    def save_entry(self) -> None:
        logma.info(f'save_entry called')
        return self

    def entryFieldModels(self) -> Any:
        logma.info(f'entryFieldModels called')
        return self

    def handler(self, key, val: dict) -> Any:
        """
        Provide data from form items via the handler in a key value pair
        :param data:
        :return:
        """
        now = dt.datetime.now()
        if key not in self.values:
            self.values[key] = {}
        self.values[key][now] = val
        return self

    def createRecord(self) -> Any:
        """"""
        fields = []
        self.record = []
        for field in fields:
            self.record.append(field[data])
        return self

    def loadControls(self) -> Any:
        """ """
        logma.info(f'New Button\n {self.entryBTNs.newbutton.__dir__()}')
        if self.entryBTNs.newbutton.isEnabled:
            self.entryBTNs.newbutton.clicked.connect(self.newEntry)
        if self.entryBTNs.submitbutton.isEnabled:
            self.entryBTNs.submitbutton.clicked.connect(self.submitEntry)
        if self.navBTNs.deletebutton.isEnabled:
            self.navBTNs.deletebutton.clicked.connect(self.deleteEntry)
        if self.navBTNs.prevbutton.isEnabled:
            self.navBTNs.prevbutton.clicked.connect(self.prevEntry)
        if self.navBTNs.jumpbutton.isEnabled:
            self.navBTNs.jumpbutton.clicked.connect(self.jumpEntry)
        if self.navBTNs.nextbutton.isEnabled:
            self.navBTNs.nextbutton.clicked.connect(self.nextEntry)
        return self

    def _build_controls(self, y=0, x=0) -> Any:
        """"""
        max_grid_x = self.config.dikt.get('max_x', x)
        return y

    def _build_fields(self, y=0, x=0, max_grid_x=1) -> Any:
        """"""
        for i, field in enumerate(self.config.dikt.get('fields', {}).keys()):
            logma.info(f'Field {field}')
            cfg = self.config.dikt['fields'][field].copy() if isinstance(self.config.dikt['fields'][field], dict) else {}
            if 'label' not in cfg:
                cfg['label'] = field
            if isinstance(cfg, dict):
                if cfg.get('store', ''):
                    table = cfg['store'][cfg['store'].find('.') + 1:cfg['store'].find('|')]
                else:
                    table = 'form'
                db_field = f'{table}.{field}'
                grid_x, grid_y = (0, y + i)
                if cfg.get('grid'):
                    if '|' in str(cfg['grid']):
                        grid_y = int(cfg['grid'][:cfg['grid'].find('|')]) + y
                        grid_x = int(cfg['grid'][cfg['grid'].find('|') + 1:])
                        max_grid_x = grid_x if grid_x > max_grid_x else max_grid_x
                        self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                        self.fieldWDGTs[db_field].initWidget()
                        self.layout.addWidget(self.fieldWDGTs[db_field], grid_y, grid_x)
                    else:
                        grid_y = int(cfg['grid']) + y
                        self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                        self.fieldWDGTs[db_field].initWidget()
                        self.layout.addWidget(self.fieldWDGTs[db_field], grid_y, 0, 1, max_grid_x)
                else:
                    self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                    self.fieldWDGTs[db_field].initWidget()
                    self.layout.addWidget(self.fieldWDGTs[db_field], y + i, 0, 1, max_grid_x)
        return y

class NchantdAPIEntryForm(NchantdDynamicEntryForm):
    """ """

    def __init__(self, parent=None, cfg={}) -> None:
        """ """
        self.config = kahndor.Instruct(pxcfg).select('NchantdAPIEntryForm')
        self.config.override(cfg)
        if parent:
            self.config.override(parent.config)
        self.src = parent.src
        super().__init__(parent, self.config)
        self.buildPane()
'\n'