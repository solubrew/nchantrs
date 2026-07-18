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
import math

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.utilities.utils import lookup
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from nchantrs.widgets.media.images import NchantdImage
from kahndor.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "annotations.yaml")


class NchantdLabel(NchantdWidgetMixin, pyqt.QLabel):
    """Standard Nchantd Label"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdLabel").override(self.parent.config).override(cfg)

    def initModel(self, cfg=None):
        """ """
        super().initModel()
        return self

    def initView(self, cfg=None):
        """ """
        self.config.override(cfg)
        self.text_wrap_limit = self.config.dikt.get("wrap_limit", 60)
        self.text = self.config.dikt.get("text", None)
        if self.text is None:
            self.text = self.config.dikt.get("label", "Missing Label")
        if not isinstance(self.text, dict):
            self.setText(str(self.text))
        else:
            raise Exception(f"Text Dictionary Provided {self.text}")
        if self.text is not None:
            if len(str(self.text)) > self.text_wrap_limit or "\n" in self.text:
                self.setWordWrap(True)
        icon_path_text = self.config.dikt.get("icon_txt", self.config.dikt.get("icon", None))
        if icon_path_text is not None:
            icon_path = self.app.view.theme.get_icon_path(icon_path_text, "base")
            image = NchantdImage(self, {"path": icon_path}).initWidget()
            width = self.config.dikt.get("width", 24)
            if width is None:
                width = 24
            height = self.config.dikt.get("height", 24)
            if height is None:
                height = 24
            width = 32
            height = 32
            image.image.scaled(width, width)
            # self.setPixmap(pyqt.QPixmap(image.image))
            icon = pyqt.QIcon(image.image)
            self.setPixmap(icon.pixmap(width, width))
            self.set_size(width, height)
        else:
            self.set_size()
        if self.config.dikt.get("tip_txt", None):
            self.setToolTip(self.config.dikt["tip_txt"])
        self.setAlignment(pyqt.Qt.AlignmentFlag.AlignCenter)
        return self

    def initWidget(self, cfg=None):
        """ """
        self.initModel(cfg)
        self.initView(cfg)
        return self

    def set_size(self, set_width=None, set_height=None, min_width=10, min_height=10, max_width=None, max_height=None):
        """"""
        text_width, text_height = self._get_text_size(self.text)
        width = text_width
        height = text_height
        logma.info(f"Text Width {text_width} Height {text_height}")
        size = self.config.dikt.get("size", None)
        if isinstance(size, list):
            width = size[0]
            height = size[1]
        if width != "auto":
            if size is None or len(size) != 2:
                size = [0, 0]
            size_width, size_height = size
            if set_width is None:
                set_width = max(text_width, size_width)
                if self.wordWrap():
                    if set_width > self.text_wrap_limit:
                        set_width = self.text_wrap_limit
        if height != "auto":
            if size is None or len(size) != 2:
                size = [0, 0]
            size_width, size_height = size
            if set_height is None:
                set_height = max(text_height, size_height)
        logma.info(f"Text Size {set_width} {set_height}")
        super().set_size(set_width, set_height, min_width, min_height, max_width, max_height)
        if self.wordWrap():
            if self.min_height is None:
                self.min_height = 30
            self.min_height = self.min_height * math.ceil(len(self.text) / self.text_wrap_limit)
            self.setMinimumHeight(self.min_height)
            logma.info(f"Min Height {self.min_height}")
        # logma.info(f"Text Length {len(self.text)}")


class NchantdBadgeBar(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdBadgeBar").override(cfg))
        self.badges = {}

    def initModel(self, actions=None):
        """"""
        super().initModel()
        if actions is None:
            actions = self.config.dikt.get("actions", None)
        if actions is not None:
            self.set_actions(actions)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        logma.info(f"Action Items {self.actions}")
        for action, button_cfg in self.actions.items():
            if isinstance(action, int):
                sequence = action
            if isinstance(button_cfg, str):
                action = button_cfg
                if button_cfg[0] == "_":  # implement an internal triger
                    if button_cfg == "_insert_stretch":
                        self.layout.addStretch()
                        continue
                    continue
            elif isinstance(button_cfg, dict):
                action = button_cfg.get("action", button_cfg.get("name", None))
            if action is None:
                continue
            self.badges[action] = {}
            action_cfg = kahndor.Instruct(lookup(self.app, action)).override(self.config)
            if isinstance(button_cfg, dict):
                action_cfg.override(button_cfg)
            self.badges[action]["widget"] = NchantdLabel(self, action_cfg)
            self.badges[action]["widget"].initWidget()
            self.layout.addWidget(self.badges[action]["widget"])

            # self.badges[action]["widget"].layout.setContentsMargins(0, 0, 0, 0)
            # self.badges[action]["widget"].layout.setSpacing(3)
        if self.config.dikt.get("justify", None) is None:
            self.layout.setAlignment(pyqt.Qt.AlignmentFlag.AlignLeft | pyqt.Qt.AlignmentFlag.AlignTop)
        else:
            self._set_alignment()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(3)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def set_actions(self, actions=None):
        """"""
        if actions is None:
            actions = self.config.dikt.get("actions", {})
        self.actions = actions
        return self


class NchantdCurrentTimeWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdCurrentTimeWidget").override(cfg))

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


class NchantdDisplayBox(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdEntryBox").override(cfg))

    def initModel(self):
        """ """
        super().initModel()
        return self

    def initView(self):
        """ """
        super().initView()
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self


class NchantdHighLowLabel(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdHighLowLabel").override(cfg))

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        layout = pyqt.QHBoxLayout()
        cfg = {"text": self.config.dikt.get("text", "")}
        label = NchantdLabel(self, cfg).initWidget()
        layout.addWidget(label)
        hl_layout = pyqt.QVBoxLayout()
        cfg = {"text": self.config.dikt.get("high", "")}
        high = NchantdLabel(self, cfg).initWidget()
        hl_layout.addWidget(high)
        cfg = {"text": self.config.dikt.get("low", "")}
        low = NchantdLabel(self, cfg).initWidget()
        hl_layout.addWidget(low)
        layout.addLayout(hl_layout)
        self.layout.addLayout(layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdProgressBar(NchantdWidgetMixin, pyqt.QProgressBar):
    def __init__(self, parent=None, cfg={}):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdEntryBox").override(cfg)
        self.setValue(0)

    def initModel(self):
        """ """
        super().initModel()
        return self

    def initView(self):
        """ """
        super().initView()
        return self

    def initWidget(self):
        """ """
        self.initModel()
        self.initView()
        return self
    def updateProgress(self):
        """ """
        return self

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
