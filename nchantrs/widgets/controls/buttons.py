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

from os.path import abspath, dirname, join
import json as j
from typing import Any, Optional, Dict
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
from kahndor.logma import Logma

here = join(dirname(__file__), "")
logma = Logma(__name__)
log = False
if not log:
    logma.off()
DEFAULT_ICON_SIZE: int = 24
LARGE_ICON_SIZE: int = 32
MIN_DIMENSION: int = 10
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

    def __init__(self, parent: Optional[Any] = None, cfg: Optional[Dict] = None) -> None:
        """Create a button widget and set default configurations"""
        super().__init__(parent=parent)
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdButton").override(parent.config).override(cfg)
        self.action: Optional[Any] = None
        self.button_text: Optional[str] = None
        self.data: Optional[Any] = None
        self.endabled: Optional[bool] = None
        self.stati: Optional[Dict] = None
        self.parameters: Optional[Dict] = {}
        self.enabled: bool = False

    def initModel(self) -> "NchantdButton":
        """

        Action is currently the top override for configurations for the button

        :return:
        """
        super().initModel()
        parameters_dikt = self.config.dikt.get("parameters_dict", "{}").replace("'", '"')
        logma.info(f"Parameters Dict {parameters_dikt}")
        if parameters_dikt == "":
            parameters_dikt = "{}"
        self.parameters = j.loads(parameters_dikt)
        self.stati = self.parameters.get("stati", {})
        self.enabled = False
        return self

    def initView(self, handler: Optional[Any] = None, text: Optional[str] = None, cfg=None) -> "NchantdButton":
        """"""
        super().initView(cfg)
        self.setCheckable(self.config.dikt.get("checkable", False))
        if self.config.dikt.get("checkable", False):
            self.setChecked(False)
        self.setEnabled(self.config.dikt.get("enabled", False))
        self.setAutoDefault(self.config.dikt.get("auto_default", None))
        self.button_text = self.config.dikt.get("text", None)
        logma.info(f"Button Text {self.button_text}")
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
            # self.set_size(None, None)
        else:
            pass
        if self.config.dikt.get("tip_txt", None):
            self.setToolTip(self.config.dikt["tip_txt"])
        self.set_handler(handler)
        self.initialize_context_menu()
        return self

    def initWidget(self, handler: Optional[Any] = None, text: Optional[str] = None) -> "NchantdButton":
        """"""
        self.initModel()
        if not handler:
            handler = self.config.dikt.get("handler", None)
        self.initView(handler, text)
        return self

    def flip(self) -> "NchantdButton":
        """"""
        if self.enabled is False:
            if "enabled" in self.stati.keys():
                self.load_image(self.stati["enabled"].get("icon", None))
            self.enabled = True
        else:
            self.load_image(self.config.dikt.get("icon_txt", self.config.dikt.get("icon", None)))
            self.enabled = False
        return self

    def load_image(self, icon_path_text: Optional[str]) -> "NchantdButton":
        """"""
        icon_path = self.app.view.theme.get_icon_path(icon_path_text, "base")
        logma.info(f"Icon Path {icon_path}")
        image = NchantdImage(self, {"path": icon_path}).initWidget()
        width = self.config.dikt.get("width", DEFAULT_ICON_SIZE)
        if width is None:
            width = DEFAULT_ICON_SIZE
        height = self.config.dikt.get("height", DEFAULT_ICON_SIZE)
        if height is None:
            height = DEFAULT_ICON_SIZE
        width = LARGE_ICON_SIZE
        height = LARGE_ICON_SIZE
        image.image.scaled(width, width)
        self.setIcon(pyqt.QIcon(image.image))
        self.setIconSize(pyqt.QSize(width, width))
        # self.set_size(width, height)
        return self

    def on_click(self, signal: Any, handler: Optional[Any] = None, params: Optional[Dict] = None) -> "NchantdButton":
        """"""
        logma.info(f"Button Clicked {self.button_text} {signal}")
        logma.info(f"Handler {handler}")
        if params is None:
            params = {}
        params["action"] = self.action
        logma.info(f"Params {params}")
        if handler:
            handler(signal, params)
        self.flip()
        return self

    def set_handler(self, handler: Optional[Any] = None, params: Optional[Dict] = None) -> "NchantdButton":
        """"""
        super().set_handler(handler, params)
        if handler:
            self.clicked.connect(lambda checked: self.on_click(checked, handler, params))
        return self

    # def set_size(self, set_width: Optional[int]=None, set_height: Optional[int]=None, min_width: int=MIN_DIMENSION, min_height: int=MIN_DIMENSION, max_width: Optional[int]=None, max_height: Optional[int]=None) -> None:
    #     """"""
    #     min_width, min_height = self._get_text_size(self.config.dikt.get('label', self.config.dikt.get('text', '')))
    #     super().set_size(set_width, set_height, min_width, min_height, max_width, max_height)


class NchantdButtonWidget(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdButtonWidget").override(cfg))
        self.button = None

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)

    def initView(self, cfg=None) -> None:
        """"""
        super().initView(cfg)
        self.button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.button)

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()


class NchantdLabeledButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdLabeledButton").override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        cfg = cfg or {}
        super().initModel(cfg)
        return self

    def initView(self) -> Any:
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
        # layout.setAlignment(getAlignment(self.config.dikt["justify"]))
        self.setLayout(layout)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdSaveButton(NchantdButton):
    """A single pane widget with a button set for submitting a form"""

    def __init__(self, parent=None, cfg={}) -> None:
        """ """
        super().__init__(parent, self.config.dikt["buttons"]["save"])
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdSaveButton").override(cfg))
        self.src = self.parent.store

    def initWidget(self, handler) -> Any:
        """ """
        super().initWidget(handler)
        return self

    def save(self, input_value) -> None:
        """
        Need to collect all data from active widgets

        :param input_value:
        :return:

        """
        logma.info(f"Input Value {input_value}")
        self.src.add(input_value, "db")


class NchantdSliderButton(NchantdWidgetMixin, pyqt.QSlider):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm"""
        super().__init__(cfg["name"])
        self.config = kahndor.Instruct(pxcfg).select("NchantdSliderButton").override(cfg)
        self.parent = parent
        self.init_variables()
        self.setMinimum(cfg["min"])
        self.setMaximum(cfg["max"])
        self.setSingleStep(cfg["step"])
        self.setValue(cfg["default_value"])
        self.setTickInterval(cfg["tickinterval"])
        self.setTickPosition(cfg["tickposition"])


class NchantdTextButton(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdTextButton").override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdDynamicTextButton(NchantdTextButton):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdDynamicTextButton").override(cfg))

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self
