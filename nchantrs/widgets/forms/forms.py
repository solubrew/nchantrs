# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>: #								||
	DOCid: 'b0383757-eb6b-4d01-a5af-f0b4bc6b3b44' #								||
	name: Nchantrs Module Widgets Forms Python Excecution Document  #			||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, join

# ===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.widgets import loadWidget
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()

# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "forms.yaml")
pxcfg = {}


class NchantdForm(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdForm"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDynamicEntryForm(NchantdForm):
    """A single pane widget for building a simple top down entry form with a
    submission button at the end of the form"""

    def __init__(self, parent=None, cfg={}):
        """

        :param parent:
        :param cfg:
        """
        super().__init__(parent, cfg)
        logma.info(f"Init NchantdDynamicEntryForm Config {cfg}")
        self.parent = parent
        self.config.override(pxcfg).select("NchantdDynamicEntryForm").override(cfg)
        self.fieldWDGTs = {}
        self.controlWDGTs = {}
        self.handlers = {}

    def initModel(self, cfg=None):
        """"""
        super().initModel()
        for control in self.config.dikt.get("controls", {}).keys():
            handler = self.config.dikt["controls"].get(control, {}).get("handler", "default")
            self.handlers[control] = getattr(self, handler)
        # self.source = self.config.dikt.get("source", "")[: self.config.dikt.get("source", "").find(".")]
        # left = -self.config.dikt.get("source", "").find(".")
        # right = self.config.dikt.get("source", "").find(".")
        # self.table = self.config.dikt.get("source", "")[left:right]
        # self.src = self.app.model.store
        self.values = {}
        self.handlers = {}
        self.rid = None
        return self

    def initView(self):
        """The pane is built with fields not sure how to abstract this

        TODO: need to get max columns grid in order to span other fields
        """
        super().initView({"layout": "grid"})
        x, y = 0, 0
        y = self._build_controls(y, x)
        y += 1
        self._build_fields(y)
        # self.setLayout(layout)
        return self

    def initWidget(self):
        """ """
        # not to create a dialog model to replace this and mimic application models
        self.reset = None
        self.initModel(self.reset)
        self.initView()
        return self

    def add_entry(self):
        """ """
        self.rid = self.app.model.store.add(self.values)
        return self

    def delete_entry(self, record):
        """ """
        self.model.deleteRecord(record)
        return self

    def jump_entry(self, record):
        """ """
        self.model.getRecord(record)
        return self

    def next_entry(self):
        """ """
        self.rid = self.app.model.store.next(self.rid)

    def previous_entry(self):
        """ """
        self.rid = self.app.model.store.prev(self.rid)

    def cancel_entry(self):
        """ """
        self.rid = None

    def save_entry(self):
        """"""

    def entryFieldModels(self):
        """Combine and connect to the dynamic entry fields and controls in
        the form"""
        return self

    def handler(self, key, val: dict):
        """
        Provide data from form items via the handler in a key value pair
        :param data:
        :return:
        """
        now = dt.datetime.now()
        if key not in self.values:
            self.values[key] = {}  # can i get the original value?
        self.values[key][now] = val
        return self

    def createRecord(self):
        """"""
        fields = []
        self.record = []
        for field in fields:
            self.record.append(field[data])
        return self

    def loadControls(self):
        """ """
        logma.info(f"New Button\n {self.entryBTNs.newbutton.__dir__()}")
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

    def _build_controls(self, y=0, x=0):
        """"""
        [DONE]
        max_grid_x = self.config.dikt.get("max_x", x)
        # for i, control in enumerate(self.config.dikt.get("controls", {})):
        #     cfg = self.config.dikt["controls"][control]
        #     self.controlWDGTs[control] = loadWidget(self, cfg)
        #     self.controlWDGTs[control].initWidget(self.model.handlers[control])
        #     self.layout.addWidget(self.controlWDGTs[control], y, x, 1, max_grid_x)
        #    y += i
        return y

    def _build_fields(self, y=0, x=0, max_grid_x=1):
        """"""
        for i, field in enumerate(self.config.dikt.get("fields", {}).keys()):
            logma.info(f"Field {field}")
            cfg = (
                self.config.dikt["fields"][field].copy() if isinstance(self.config.dikt["fields"][field], dict) else {}
            )
            # Add the field name to the configuration so the widget can display it as a label
            if "label" not in cfg:
                cfg["label"] = field
            if isinstance(cfg, dict):
                if cfg.get("store", ""):
                    table = cfg["store"][cfg["store"].find(".") + 1 : cfg["store"].find("|")]
                else:
                    table = "form"
                db_field = f"{table}.{field}"
                grid_x, grid_y = 0, y + i
                if cfg.get("grid"):
                    if "|" in str(cfg["grid"]):
                        grid_y = int(cfg["grid"][: cfg["grid"].find("|")]) + y
                        grid_x = int(cfg["grid"][cfg["grid"].find("|") + 1 :])
                        max_grid_x = grid_x if grid_x > max_grid_x else max_grid_x
                        self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                        self.fieldWDGTs[db_field].initWidget()
                        self.layout.addWidget(self.fieldWDGTs[db_field], grid_y, grid_x)
                    else:
                        grid_y = int(cfg["grid"]) + y
                        self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                        self.fieldWDGTs[db_field].initWidget()
                        self.layout.addWidget(self.fieldWDGTs[db_field], grid_y, 0, 1, max_grid_x)
                else:
                    # Add field with default grid position if grid not specified
                    self.fieldWDGTs[db_field] = loadWidget(self, cfg)
                    self.fieldWDGTs[db_field].initWidget()
                    self.layout.addWidget(self.fieldWDGTs[db_field], y + i, 0, 1, max_grid_x)
        return y


class NchantdAPIEntryForm(NchantdDynamicEntryForm):
    """ """

    def __init__(self, parent=None, cfg={}):
        """ """
        self.config = condor.Instruct(pxcfg).select("NchantdAPIEntryForm")
        self.config.override(cfg)
        if parent:
            self.config.override(parent.config)
        self.src = parent.src
        super().__init__(parent, self.config)
        self.buildPane()


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
