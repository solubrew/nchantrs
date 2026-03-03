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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.widgets.widgets import NchantdWidget
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "managers.yaml")
pxcfg = {}


class NchantdManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdManager"))
        # if self.parent:
        #     self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
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


class NchantdBasket(NchantdWidget):
    """A Group with configuration drop in actions like moving, or copying a file, exporting, importing, tagging
    etc"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdBasket")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
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


class NchantdBasketManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdBasketManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdBasketManager, self).__init__(self.parent, self.config)
        self.baskets = ["Memes", "InfoGraphics", "Photos"]

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        for basket in self.baskets:
            group = pyqt.QGroupBox()
            group.setTitle(basket)
            layout = pyqt.QVBoxLayout()
            group.setLayout(layout)
            cfg = {"text": "Drop File Here"}
            label = NchantdLabel(self, cfg).initWidget()
            layout.addWidget(label)
            self.layout.addWidget(group)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdExtensionManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdExtensionManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdExtensionManager, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        header_layout = pyqt.QVBoxLayout()
        cfg = {}
        self.header = NchantdLabel(self, cfg).initWidget()
        header_layout.addWidget(self.header)
        self.layout.addLayout(header_layout)
        self.extension_catalog = NchantdCatalog(self, cfg).initWidget()
        self.layout.addWidget(self.extension_catalog)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def add_extension(self):
        """
        need a method for injecting tabs into tabsets for specific nodes
        those nodes could be

        singlely identified or
        pattern identified or
        a mapping

        :return:
        """

    def remove_extension(self):
        """"""


class NchantdFileSystemsManager(NchantdManager):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFileSystemsManager")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        super(NchantdFileSystemsManager, self).__init__(self.parent, self.config)

    def initModel(self):
        """"""
        return self

    def initView(self):
        """"""
        layout = pyqt.QHBoxLayout()
        cfg = {}
        table = NchantdFileSystemsTable(self, cfg).initWidget()
        layout.addWidget(table)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdSecurityManager(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("Nchantd"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
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


# class SecureBrowserWindow(QMainWindow):
#     """Main browser window with integrated security"""
#
#     def __init__(self, security_manager: CrossPlatformSecurityManager):
#         super().__init__()
#
#         self.security_manager = security_manager
#
#         # Create secure profile
#         self.profile = SecureWebProfile("SecureProfile", security_manager)
#
#         # Setup UI
#         self._setup_ui()
#
#         # Apply platform-specific window security
#         self._apply_window_security()
#
#     def _setup_ui(self):
#         """Setup the user interface"""
#
#         # Central widget
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         # Layout
#         layout = QVBoxLayout(central_widget)
#
#         # Web view with secure profile
#         self.web_view = QWebEngineView()
#         self.web_view.page().setProfile(self.profile)
#
#         layout.addWidget(self.web_view)
#
#         # Set window properties
#         self.setWindowTitle(f"Secure Browser - {self.security_manager.security_config['security_level'].title()}")
#         self.resize(1200, 800)
#
#     def _apply_window_security(self):
#         """Apply platform-specific window security measures"""
#
#         security_level = self.security_manager.security_config["security_level"]
#
#         if security_level == "maximum":
#             # Maximum security: prevent screenshots/recording
#             if self.security_manager.os_type == OSType.WINDOWS:
#                 # Windows: Set window as protected content
#                 try:
#                     import ctypes
#                     from ctypes import wintypes
#
#                     hwnd = int(self.winId())
#                     ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x11)  # WDA_EXCLUDEFROMCAPTURE
#                 except:
#                     print("Could not set window protection on Windows")
#
#         # Disable context menus for security
#         self.web_view.setContextMenuPolicy(self.web_view.contextMenuPolicy().NoContextMenu)
#
#     def load_url(self, url: str):
#         """Load URL with security validation"""
#
#         # Validate URL before loading
#         if not self._is_url_safe(url):
#             print(f"URL blocked by security policy: {url}")
#             return
#
#         self.web_view.load(QUrl(url))
#
#     def _is_url_safe(self, url: str) -> bool:
#         """Validate if URL is safe to load"""
#
#         # Basic URL validation
#         if not url.startswith(("http://", "https://", "data:")):
#             return False
#
#         # Security level specific validation
#         security_level = self.security_manager.security_config["security_level"]
#
#         if security_level == "maximum" and not url.startswith("https://"):
#             return False  # Only HTTPS in maximum security
#
#         return True


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
