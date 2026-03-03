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
import json as j

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
debug = True
logma.off()
# ====================================================================================================================||
pxcfg = join(here, "_data_", "buttons.yaml")


class NchantdButton(NchantdWidgetMixin, pyqt.QPushButton):
    """A custom button widget that inherits from QPushButton.

    The NchantdButton class provides a button widget with configurable properties and methods.

    Attributes:
        config (ConfigObj): A configuration object that contains the button's configuration settings.
        parent (QWidget): The parent widget to which the button belongs.

    Methods:
        __init__(parent=None, cfg={}): Initializes the NchantdButton object with default configurations.
        initWidget(handler=None): Initializes the widget with the specified configuration settings and connects the specified handler to the button's clicked signal.
    """

    def __init__(self, parent=None, cfg=None):
        """Create a button widget and set default configurations"""
        super().__init__(parent, cfg)
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdButton")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app = pyqt.QApplication.instance()
        self.action = None
        self.button_text = None
        self.data = None
        self.endabled = None
        self.stati = None

    def initModel(self):
        """

        Action is currently the top override for configurations for the button

        :return:
        """
        super().initModel()
        parameters_dikt = self.config.dikt.get("parameters_dict", "{}").replace("'", '"')
        # logma.info(f"Parameters Dict {parameters_dikt}")
        self.parameters = j.loads(parameters_dikt)
        self.stati = self.parameters.get("stati", {})
        self.enabled = False
        return self

    def initView(self, handler, text=None):
        """"""
        self.setCheckable(self.config.dikt.get("checkable", False))
        if self.config.dikt.get("checkable", False):
            self.setChecked(False)
        self.setEnabled(self.config.dikt.get("enabled", False))
        self.setAutoDefault(self.config.dikt.get("auto_default", None))
        self.button_text = self.config.dikt.get("text", None)
        self.config.dikt.pop("width", None)
        self.config.dikt.pop("height", None)
        self.config.dikt.pop("size", None)
        if text is not None:
            self.button_text = text
        icon_path_text = self.config.dikt.get("icon_txt", self.config.dikt.get("icon", None))
        if icon_path_text is not None:
            self.load_image(icon_path_text)
        elif self.button_text:
            self.setText(self.button_text)
            self.set_size(None, None)
        else:
            pass
        if self.config.dikt.get("tip_txt", None):
            self.setToolTip(self.config.dikt["tip_txt"])
        self.set_handler(handler)
        return self

    def initWidget(self, handler=None, text=None):
        """"""
        self.initModel()
        if not handler:
            handler = self.config.dikt.get("handler", None)
        self.initView(handler, text)
        return self

    def flip(self):
        """"""
        if self.enabled is False:
            if "enabled" in self.stati.keys():
                self.load_image(self.stati["enabled"].get("icon", None))
            self.enabled = True
        else:
            self.load_image(self.config.dikt.get("icon_txt", self.config.dikt.get("icon", None)))
            self.enabled = False
        return self

    def load_image(self, icon_path_text):
        """"""
        icon_path = self.app.view.theme.get_icon_path(icon_path_text, "base")
        logma.info(f"Icon Path {icon_path}")
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
        self.setIcon(pyqt.QIcon(image.image))
        self.setIconSize(pyqt.QSize(width, width))
        self.set_size(width, height)
        return self

    def on_click(self, signal, handler=None, params=None):
        """"""
        # TODO: refactor this whole concept
        logma.info(f"Button Clicked {self.button_text} {signal}")
        logma.info(f"Handler {handler}")  # needs change to update the pane
        # logma.info(f"App {self.app}")
        if params is None:
            params = {}
        params["action"] = self.action
        logma.info(f"Params {params}")
        if handler:
            handler(signal, params)
        self.flip()
        return self

    def set_handler(self, handler=None, params=None):
        """"""
        super().set_handler(handler, params)
        if handler:
            self.clicked.connect(lambda checked: self.on_click(checked, handler, params))
        return self

    def set_size(self, set_width=None, set_height=None, min_width=10, min_height=10, max_width=None, max_height=None):
        """"""
        min_width, min_height = self._get_text_size(self.config.dikt.get("label", self.config.dikt.get("text", "")))
        # logma.info(f"Min width {min_width} Min height {min_height}")
        super().set_size(set_width, set_height, min_width, min_height, max_width, max_height)


class NchantdLabeledButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg)
        self.config.select("NchantdLabeledButton")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        label = NchantdLabel(self, {"text": self.config.dikt["text"]}).initWidget()
        button = NchantdButton(self, {"text": self.config.dikt["label"]}).initWidget()
        if self.config.dikt["layout"] == "horizontal":
            layout = pyqt.QHBoxLayout()
        else:
            layout = pyqt.QVBoxLayout()
        logma.info(f"Nchantd Entry Editor {self.config.dikt.keys()}")
        layout.addWidget(label)
        layout.addWidget(button)
        layout.setAlignment(getAlignment(self.config.dikt["justify"]))
        self.setLayout(layout)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdSaveButton(NchantdButton):
    """A single pane widget with a button set for submitting a form"""

    def __init__(self, parent=None, cfg={}):
        """ """
        self.config = condor.Instruct(pxcfg).override(cfg)
        self.config.select("NchantdSaveButton")
        if parent:
            self.config.override(parent.config)
        self.parent = parent
        self.src = self.parent.store
        super().__init__(self, self.config.dikt["buttons"]["save"])

    def initWidget(self, handler):
        """ """
        super().initWidget(handler)
        return self

    def save(self, input_value):
        """
        Need to collect all data from active widgets

        :param input_value:
        :return:

        """
        logma.info(f"Input Value {input_value}")
        self.src.add(input_value, "db")


class NchantdSliderButton(NchantdWidgetMixin, pyqt.QSlider):
    """ """

    def __init__(self, app, cfg, parent=None):
        """https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm"""
        if parent:
            cfg = parent.config
        self.config = condor.Instruct(pxcfg).override(cfg)
        super(pyqt.QSlider, self).__init__(cfg["name"])
        self.setMinimum(cfg["min"])
        self.setMaximum(cfg["max"])
        self.setSingleStep(cfg["step"])
        self.setValue(cfg["default_value"])
        self.setTickInterval(cfg["tickinterval"])
        self.setTickPosition(cfg["tickposition"])
        self.valueChanged.connect(getattr(app, cfg["handlers"]["value_changed_handler"]))
        self.sliderPressed.connect(getattr(app, cfg["handlers"]["slider_pressed_handler"]))
        self.sliderMoved.connect(getattr(app, cfg["handlers"]["slider_moved_handler"]))
        self.sliderReleased.connect(getattr(app, cfg["handlers"]["slider_released_handler"]))


class NchantdTextButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

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


class NchantdDynamicTextButton(NchantdTextButton):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent, self.config)

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


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
