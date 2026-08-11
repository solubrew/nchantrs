from typing import Any

"\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n"
from os.path import dirname, join, exists
import base64
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.media.utilities import render_svg_to_pixmap
from kahndor.logma import Logma

here = join(dirname(__file__), "")
log = True
logma = Logma(__name__)
logma.off()
pxcfg = join(here, "_data_", "images.yaml")


class NchantdImage(NchantdWidget):
    """
    An extended widget that supports displaying images with added container size
    controls and alignment within the container.
    """

    def __init__(self, parent=None, cfg=None) -> None:
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdImage").override(cfg))
        self.default_path = join(here, "../../themes", "_data_", "img", "defaulty.jpg")
        self.file_path = None
        self.label = pyqt.QLabel(self)
        self.image = None
        self.is_scaled = None
        self.container_size = (200, 200)
        self.color = self.config.dikt.get("color", "black")
        self.color = None
        self.hex = None
        self.rgb = None
        self.min_width = None
        self.min_height = None

    def initModel(self) -> Any:
        """Initialize the model with image size and container logic."""
        super().initModel()
        self.is_scaled = self.config.dikt.get("scaled", False)
        icon_path_text = self.config.dikt.get("icon", self.config.dikt.get("icon_txt", None))
        if icon_path_text is None:
            logma.info(f"Icon path is None")
            self.set_file_path(None)
        elif exists(str(icon_path_text)):
            logma.info(f"Icon path: {icon_path_text}")
            self.set_file_path(str(icon_path_text))
        elif icon_path_text is not None:
            logma.info(f"Icon get Path: {icon_path_text}")
            icon_path = self.app.view.theme.get_icon_path(icon_path_text, "base")
            logma.info(f"Icon path: {icon_path}")
            self.set_file_path(icon_path)
        else:
            raise Exception(f"Unknown File Handling {icon_path_text} {self.config.dikt.get('icon_txt', None)}")
        return self

    def initView(self) -> Any:
        """Initialize the view of the widget."""
        super().initView()
        alignment_flag = pyqt.Qt.AlignmentFlag.AlignCenter | pyqt.Qt.AlignmentFlag.AlignCenter
        self.label.setAlignment(alignment_flag)
        self.label.setSizePolicy(pyqt.QSizePolicy.Policy.Expanding, pyqt.QSizePolicy.Policy.Expanding)
        self.label.setScaledContents(False)
        # if self.is_scaled: #TODO this was causing non ratio locked scaling of images.  testing to determine if any further changes are needed
        #     self.label.setScaledContents(True)
        if self.config.dikt.get("color"):
            self.label.setStyleSheet(f"background-color: {self.config.dikt.get('color')};")
        self.set_size()
        if self.config.dikt.get("image_data", None) is not None:
            logma.info(f"image_data {self.config.dikt.get('image_data', None)}")
            self.load_image_from_data(self.config.dikt.get("image_data", None))
        else:
            self.load_image(self.file_path, self.width_size, self.height_size)
        self.layout.addWidget(self.label)
        return self

    def initWidget(self) -> Any:
        """Initialize the widget, including model and view setup."""
        self.initModel()
        self.initView()
        return self

    def loadImage(self, path=None, size_x=None, size_y=None) -> Any:
        """"""
        logma.depricate(f"Change self.loadImage() method to self.load_image()")
        self.load_image(path)#, size_x, size_y)
        return self

    def load_image(self, path=None, size_x=None, size_y=None) -> Any:
        """Load and resize an image from the specified path."""
        if path is not None:
            self.set_file_path(path)
        path = self.file_path
        logma.info(f"Path {path}")
        logma.info(f"Path {self.config.dikt.get('path', None)}")
        if exists(path):
            if path.endswith(".svg"):
                logma.info(f"Path {path}")
                logma.info(f"Size X {size_x} Size Y {size_y}")
                if size_x == "auto":
                    size_x = self.width()
                if size_y == "auto":
                    size_y = self.height()
                self.image = render_svg_to_pixmap(path, size_x, size_y)
            elif path.endswith(".gif"):
                self.image = pyqt.QMovie(path)
            else:
                logma.info(f"Path {path}")
                self.image = pyqt.QPixmap(path)
        elif path == "Blank":
            self.image = pyqt.QPixmap(size_x, size_y)
            self.image.fill(pyqt.QColor(self.color))
        else:
            logma.error(f"Image file not found: {path}")
            return self
        self.label.setPixmap(self.image)
        self.original_pixmap = self.image
        return self

    def load_image_from_data(self, data) -> Any:
        """"""
        self.image = pyqt.QPixmap()
        self.image.loadFromData(base64.b64decode(data))
        self.label.setPixmap(self.image)
        self.original_pixmap = self.image
        return self

    def refresh(self) -> None:
        """"""
        image, cursor_pos = self.app.view.take_screen_shot()
        color = image.toImage().pixelColor(cursor_pos)
        self.color = color.name()
        self.hex = color.hex()
        self.rgb = color.rgb()

    def resizeEvent(self, event) -> None:
        if self.label.pixmap():
            source = getattr(self, "original_pixmap", None) or self.label.pixmap()
            scaled = source.scaled(
                self.label.size(),
                pyqt.Qt.AspectRatioMode.KeepAspectRatio,
                pyqt.Qt.TransformationMode.SmoothTransformation,
            )
            self.label.setPixmap(scaled)
        super().resizeEvent(event)

    def set_file_path(self, path=None) -> Any:
        """Set the file path for the image."""
        logma.info(f"Path {path}")
        if path is None:
            path = self.config.dikt.get("path", None)
        if path is None:
            path = self.config.dikt.get("file_path", None)
        if path is None:
            path = self.default_path
        self.file_path = path
        return self

    def set_size(self, width=None, height=None) -> None:
        """"""
        super().set_size(width, height)
        size_0, size_1 = (100, 100)
        if self.config.dikt.get('size'):
            if isinstance(self.config.dikt.get('size'), (list, tuple)):
                size_0, size_1 = self.config.dikt.get('size')[:2]
        if self.config.dikt.get('container_size'):
            if isinstance(self.config.dikt.get('container_size'), (list, tuple)):
                self.container_size = self.config.dikt.get('container_size')[:2]
        if size_0 is None:
            size_0 = 100
        if size_1 is None:
            size_1 = 100
        self.width_size = size_0
        self.height_size = size_1
        if width is not None and height is not None:
            if width != 'auto' and height != 'auto':
                self.image = self.image.scaled(int(self.min_width), int(self.min_height), pyqt.Qt.AspectRatioMode.KeepAspectRatio, pyqt.Qt.TransformationMode.SmoothTransformation)

    def create_pencil_sketch(self) -> None:
        """Implement pencil sketch creation (placeholder)."""
        pass

    def get_color_palette(self) -> None:
        """Implement color palette extraction (placeholder)."""
        pass


class NchantdScreenShot(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.setWindowTitle("Screenshot Tool")
        self.setWindowFlags(pyqt.Qt.FramelessWindowHint | pyqt.Qt.WindowStaysOnTopHint | pyqt.Qt.Dialog)
        self.setWindowOpacity(0.5)
        self.setAttribute(pyqt.Qt.WA_TranslucentBackground, True)
        self.setCursor(pyqt.Qt.CrossCursor)
        self.start_point = None
        self.end_point = None
        self.is_selecting = False
        self.setGeometry(0, 0, self.app.primaryScreen().size().width(), self.app.primaryScreen().size().height())
        logma.info(f"NchantdScreenShot initialized")

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

    def mousePressEvent(self, event) -> None:
        """Start selection on mouse press."""
        if event.button() == pyqt.Qt.LeftButton:
            self.start_point = event.pos()
            self.is_selecting = True

    def mouseMoveEvent(self, event) -> None:
        """Update selection as the mouse moves."""
        if self.is_selecting:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        """Finish selection and take a screenshot."""
        if event.button() == pyqt.Qt.LeftButton:
            self.end_point = event.pos()
            self.is_selecting = False
            self.take_screenshot()
            self.close()

    def paintEvent(self, event) -> None:
        """Draw the selection rectangle."""
        if self.start_point and self.end_point:
            painter = pyqt.QPainter(self)
            painter.setRenderHint(pyqt.QPainter.Antialiasing)
            pen = pyqt.QPen(pyqt.QColor(255, 0, 0), 2)
            painter.setPen(pen)
            painter.setBrush(pyqt.QColor(255, 0, 0, 50))
            rect = pyqt.QRect(self.start_point, self.end_point)
            painter.drawRect(rect)

    def take_screenshot(self) -> None:
        """Capture the selected region."""
        if not self.start_point or not self.end_point:
            return
        rect = pyqt.QRect(self.start_point, self.end_point).normalized()
        screen = self.app.primaryScreen()
        screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        screenshot.save("screenshot.png", "png")
