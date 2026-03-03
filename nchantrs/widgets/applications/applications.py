# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""  #																			||
---  #																			||
<(META)>: '3a0f63bb-96be-4c2f-bd5b-31fc64fd00b3' #								||
	docid:   #																	||
	name: Nchantrs Module Nchantrs Python Excecution Document  #				||
	description: >  #															||
		Nchantrs allows for the modular creation of a gui app via  #			||
		configuration files.  The main window holds a grid of widgets such  #	||
		that each application is its own singular document type saving, new,  #	||
		open etc refers to the data used to populate the widgets.  The  #		||
		default data format for test_nchantrs applications is yaml files with the  #	||
		ability to override with an sql storage method  #						||
		leverage PyQt5TableModels to integrate tables
	expirary: <[expiration]>  #													||
	version: 0.0.0.0.0.0  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
"""  # ||
# -*- coding: utf-8 -*-#														||
# ================================Core Modules===================================||
from os.path import abspath, dirname, exists, join, expanduser
from os import environ
from pathlib import Path
import os
from sys import argv
import platform

# ===============================================================================||

# ===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.extensions.extensions import NchantdExtensionsManager

from nchantrs.models.applicationmodels import NchantdCloakModel, NchantdPantiesModel
from nchantrs.services.services import NchantdServiceManager
from nchantrs.extensions.packages.nchantdlibrary.nchantdlibrary import NchantdLibraryManager
from nchantrs.updates.db import DBUpdate
from nchantrs.utilities.comms import NchantdCommunicationsManager
from nchantrs.views.applicationviews import NchantdCloakView, NchantdPantiesView
from nchantrs.widgets.controls.menus import NchantdContextMenu
from ogma.logma import Logma

# ===============================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
logma.off()
debug = True
# ===============================================================================||
pxcfg = join(abspath(here), "_data_", "applications.yaml")  # ||


class NchantdPanties(pyqt.QApplication):
    """
    NchantdPanties
    =============

    A class that represents an instance of the NchantdPanties application.

    Methods:
        - __init__(name, parent=None, cfg=None): Initializes an instance of the NchantdPanties class.
        - initView(): Initializes the application view.
        - initModel(): Initializes the application model.

    Attributes:
        - parent: The parent instance of the application.
        - config: The configuration for the application.
        - reset: A flag indicating whether the application needs to be reset.
        - name: The name of the application.
        - slug: A lowercase and space-separated version of the application name.
        - newInstance: A flag indicating whether a new instance of the application has been created.

    """

    config = None

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None):
        """
        Initializes an instance of the NchantdPanties class.

        :param name: The name of the instance.
        :type name: str
        :param parent: The parent instance.
        :type parent: NchantdPanties or None
        :param cfg: The configuration for the instance.
        :type cfg: dict or None
        """

        config = condor.Instruct(pxcfg).select("NchantdPanties").addArgs(args)
        if self.config is None:
            self.config = config
        else:
            self.config.override(config)
        logma.info(f"Panties Config {self.config.dikt.get('config', None)}")
        self.parent = parent
        self.config.override(cfg)
        self.application_name = name
        self.slug = self.application_name.lower().replace(" ", "_")
        super().__init__(argv)
        self.application_NCD = "da1e9bb0-1dab-48de-ac28-9afa91568a39"  # Nchantrs Core D
        self.dialogs = {}
        self.reset = None
        self.app = pyqt.QApplication.instance()
        self.model = NchantdPantiesModel(self)
        self.view = NchantdPantiesView(self)
        self.primary_focus = None
        self.is_installable = self.config.dikt.get("is_installable", False)
        self.is_install_optional = self.config.dikt.get("is_install_optional", False)
        self.is_install_selected = False
        if self.is_installable and self.is_install_optional is True:
            self.is_install_selected = self.config.dikt.get("is_install_selected", False)
        if self.is_installable and self.is_install_optional is False:
            self.is_install_selected = True
        self.is_installed = False
        self.has_agents = None
        self.agent_manager = None
        self.has_comms = None
        self.comms_manager = None
        self.has_services = None
        self.service_manager = None
        self.has_extensions = None
        self.extension_manager = None
        self.library_manager = None
        self.has_library = None
        self.new_application = None
        # self.new_instance = None
        self.new_account = None
        self.startup = None
        self.recent_documents = []
        self.version = None
        self.context_menu = None

    def initApp(self, cfg=None):
        """"""
        self.initModel()
        self.initView()
        return self

    def initModel(self, reset=None):
        """
        :return:
        """
        if reset is not None:
            self.reset = reset
        self.model.initModel(self.reset)  # ||
        return self

    def initView(self, cfg=None):
        """
        :return:
        """
        self.view.initView()
        self.model.store.store_app_event("initialized", "application view initialized")
        return self

    def initialize_configuration(self):
        """Top level Applications will implement this method in order to preemptively modify any base configurations
        this will also be the code used to establisht the application bootstrapping configs
        """

    def initialize_context_menu(self):
        """"""
        cfg = {"actions": self.config.dikt.get("menus", {}).get("actions", [{"action": "No Context", "handler": None}])}
        self.context_menu = NchantdContextMenu(self, cfg).initWidget()
        return self

    def launch_dialog(self, dialog_name, name_override=None):
        """"""
        name = dialog_name
        if name_override is not None:
            name = name_override
        self.dialogs[name] = get_dialog(dialog_name)
        self.dialogs[name](self, self.config)
        self.dialogs[name].initWidget()
        return self

    def __getstate__(self):
        """"""
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        if state.get("unpickable_attribute", False):
            del state["unpicklable_attribute"]
        return state

    def __setstate__(self, state):
        """"""


class NchantdCloak(NchantdPanties):  # ||
    """
    NchantdCloak class.
    Initialize the application and the database then update all sink
    data tables from the established source endpoints.
    Attributes:
        config (Config): The configuration object.
        main (pyqt.QtGui.QMainWindow): The main application window.
        model (NchantdCloakModel): The model object.
        view (NchantdCloakView): The view object.
        newApp (bool): Indicates if it is a new application. This will be used to allow multiple Nchantrs based
                       applications to be ran at the same time.  As well as supporting the future ability to load
                       applications as addons/files within an app or opening the same as its own program or file.
        dialogs (dict): The dictionary of dialogs.
    """

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None):
        """Initialize the application and the database then update all sink
        data tables from the established source endpoints"""
        super().__init__(name, instance, parent)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdCloak"))
        self.config.addArgs(args).override(cfg)
        self.main = NchantdMainWindow(self)
        self.model = NchantdCloakModel(self)
        self.view = NchantdCloakView(self)
        self.dbupdate = DBUpdate(self)

    def initApp(self, cfg=None):  # ||
        """Initialize UI setting the main application layout and building
        landing widgets
        Load Pane based on the selection in the navigation tree"""
        # TODO: update to each DELTA level not sure best way to keep this in sync for new files
        self.system = platform.system().lower()
        self.set_version(self.config.dikt.get("config", {}).get("version", "0.0.1.0.1.0"))
        if self.has_agents is None:
            self.has_agents = self.config.dikt["config"].get("has_agents", False)
        self.agent_manager = None
        if self.has_comms is None:
            self.has_comms = self.config.dikt["config"].get("has_comms", False)
        self.comms_manager = None
        if self.has_services is None:
            self.has_services = self.config.dikt["config"].get("has_services", False)
        self.service_manager = None
        if self.has_extensions is None:
            self.has_extensions = self.config.dikt["config"].get("has_extensions", False)
        self.extension_manager = None
        if self.has_library is None:
            self.has_library = self.config.dikt["config"].get("has_library", False)
        self.library_manager = None
        self.init_managers()
        self.config.override(cfg)
        self.startup = self.config.dikt["startup"]
        self.new_application = self.startup.new_application
        self.initModel()  # TODO eventually this will need to be put into a seperate process
        self.initView()
        pyqt.QTimer.singleShot(0, self.set_initial_state)
        try:
            self.exec_()  # this is inherited from the pyqt.QApplication class
        except Exception as e:
            if self.has_comms:
                if self.comms_manager.notice_app_failed(e) == "restart":
                    self.comms_manager.request_restart()
        return self

    def initModel(self, reset=None):
        """"""
        super().initModel(reset)
        # TODO: environment variables do not seem to address any of the issues with codec loading
        #  will leave code in place for now but will need to revisit later
        # self.set_environment_variables(join(expanduser("~"), ".local", "share", "nchantdoffice"))
        return self

    def initView(self):
        """
        Initializes the view.

        :return: None
        """
        # TODO: work out the preload browser logic
        super().initView()
        self.main.setup_shortcuts()
        return self

    def init_managers(self):
        """"""
        if self.has_agents:
            cfg = {}
            self.agent_manager = NchantdSentinelManager(self, cfg)
            # self.agent_manager.initManager()
        if self.has_comms:
            cfg = {}
            self.comms_manager = NchantdCommunicationsManager(self, cfg)
            self.comms_manager.initManager()
        # if self.has_securit:
        #     cfg = {}
        #     self.security_manager = NchantdSecurityManager()
        #     self.security_manager.initManager()
        if self.has_services:
            cfg = {}
            self.service_manager = NchantdServiceManager(self, cfg)
            # self.service_manager.initManager()
        if self.has_extensions:
            cfg = {}
            self.extension_manager = NchantdExtensionsManager(self, cfg)
            # self.extension_manager.initManager()
        if self.has_library:
            cfg = {}
            self.library_manager = NchantdLibraryManager(self, cfg)
            # self.library_manager.initManager()
        return self

    def get_current_version(self):
        """"""
        return self.model.get_current_version()

    def run_on_launch(self):
        """"""

    def set_initial_state(self):
        """"""
        # logma.info(f"Application Initial Action")
        self.run_on_launch()
        pane = self.view.panes["left"].tree
        pane.model.current_node.updateTabs("center")
        pane.model.current_node.updateTabs("right")
        pane.refresh()
        return self

    def set_version(self, version):
        """"""
        if version is None:
            version = "0.0.1.0.1.0"
        self.version = version
        return self

    def set_environment_variables(self, library_path):
        """Set environment variables for Chromium WebEngine."""
        if isinstance(library_path, str):
            library_path = Path(library_path)

        logma.info(f"Setting Environment Variables for Nchantd Office")
        logma.info(f"library_path: {library_path}")

        chromium_flags = self._build_chromium_flags(library_path)
        environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(chromium_flags)

        ozone_platform = detect_linux_display_system()
        logma.info(f"ozone_platform: {ozone_platform}")
        # logma.info(f"Library Parent {library_path.parent}")

    def _build_chromium_flags(self, library_path):
        """Build Chromium flags based on platform and configuration."""
        codec_path_drm, codec_path_h264 = self._get_codec_paths()
        cache_name = "cache"  # Extract variable for cache directory name

        # Core flags for OpenH264 support
        base_flags = [
            # OpenH264 specific configuration
            f"--openh264-path={codec_path_h264}",
            "--enable-features=WebRTCUseH264",
            "--enable-features=RTCUseH264",
            "--force-fieldtrials=WebRTC-H264WithOpenH264FFmpeg/Enabled/",
            # Media decoding optimization
            "--enable-accelerated-video-decode",
            "--enable-accelerated-mjpeg-decode",
            "--disable-features=UseChromeOSDirectVideoDecoder",  # Use OpenH264 instead of system decoder
            # WebRTC and media streaming
            "--enable-features=WebRTCHideLocalIpsWithMdns",
            "--enable-features=WebRTCAllowInputVolumeAdjustment",
            "--enable-webrtc-stun-origin",
            # Memory and performance optimization
            "--max-decoded-image-size-mb=512",
            "--enable-gpu-memory-buffer-video-frames",
            "--enable-zero-copy",
            "--enable-checker-imaging",
            # Application-specific paths
            f"--user-data-dir={self.model.app_path}/.persistence",
            f"--disk-cache-dir={self.model.app_path}/{cache_name}/Cache",
            f"--log-file={self.model.app_path}/logs/chromium.log",
            # Security (safer alternatives to --no-sandbox)
            "--disable-dev-shm-usage",  # Helps with resource constraints
            "--disable-gpu-process-for-dx12-vulkan-info-collection",
            "--disable-backgrounding-occluded-windows",
            # Stability and compatibility
            "--disable-features=VizDisplayCompositor",  # Can cause issues with video
            "--disable-gpu-process-crash-limit",
            "--ignore-gpu-blocklist",
            "--disable-software-rasterizer",
        ]
        if debug:
            base_flags.extend(
                [
                    # Debugging (remove in production)
                    "--enable-logging=stderr",
                    "--log-level=1",
                    "--enable-features=LogJsConsoleMessages",
                ]
            )
        # Platform-specific optimizations
        if self.system == "linux":
            linux_flags = [
                # Hardware acceleration for Linux
                "--enable-features=VaapiVideoDecoder,VaapiVideoEncoder,VaapiIgnoreDriverChecks",
                "--enable-hardware-overlays=single-fullscreen,single-on-top,underlay",
                "--enable-gpu-rasterization",
                # Display server detection
                # f"--ozone-platform={self._detect_display_system()}",
                # (
                #     "--enable-features=UseOzonePlatform"
                #     if self._should_use_ozone()
                #     else "--disable-features=UseOzonePlatform"
                # ),
                "--disable-features=UseOzonePlatform",
                # Audio system
                "--enable-features=PulseaudioLoopbackForCast,PulseaudioLoopbackForScreenShare",
                # Sandbox configuration (safer than complete disable)
                "--disable-seccomp-filter-sandbox" if self._needs_sandbox_relaxation() else "",
            ]
            base_flags.extend([f for f in linux_flags if f])  # Filter empty strings

        elif self.system == "windows":
            windows_flags = [
                # Windows Media Foundation support
                "--enable-features=MediaFoundationH264Encoding",
                "--enable-win32k-renderer-lockdown",
                "--enable-features=D3D11VideoDecoder",
                "--disable-d3d11",  # Sometimes needed for codec compatibility
                # Windows-specific OpenH264
                "--enable-media-foundation-async-h264-encoding",
            ]
            base_flags.extend(windows_flags)

        elif self.system == "darwin":  # macOS
            macos_flags = [
                # VideoToolbox hardware acceleration
                "--enable-features=VideoToolboxVP9Decoder",
                "--enable-videotoolbox-av1-decoding",
                "--disable-metal-test-shaders",  # Can interfere with video
            ]
            base_flags.extend(macos_flags)

        # Remove any empty flags and duplicates
        return list(filter(None, list(dict.fromkeys(base_flags))))

    def _detect_display_system(self):
        """Detect the appropriate display system for Linux."""
        if hasattr(self, "_display_system"):
            return self._display_system

        from os import environ

        # Check environment variables first
        if environ.get("WAYLAND_DISPLAY"):
            self._display_system = "wayland"
        elif environ.get("DISPLAY"):
            self._display_system = "x11"
        else:
            # Check for running display servers
            try:
                import subprocess

                # Check if Wayland compositor is running
                result = subprocess.run(
                    ["pgrep", "-f", "(wayland|sway|weston)"], capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0:
                    self._display_system = "wayland"
                else:
                    self._display_system = "x11"
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                self._display_system = "x11"  # Safe default

        return self._display_system

    def _should_use_ozone(self):
        """Determine if Ozone platform should be used."""
        display_system = self._detect_display_system()
        return display_system == "wayland"

    def _needs_sandbox_relaxation(self):
        """Check if sandbox needs to be relaxed for codec access."""
        # Only relax sandbox if absolutely necessary
        # This could check for specific system configurations that require it
        try:
            # Test if we can access the codec file with current permissions
            codec_path_drm, codec_path_h264 = self._get_codec_paths()
            return not os.access(codec_path_h264, os.R_OK)
        except:
            return True  # If we can't check, err on the side of relaxation

    def _get_codec_paths(self):
        """Get platform-specific codec paths for runtime-downloaded OpenH264."""

        if self.system == "linux":
            architecture = platform.machine()
            if architecture == "x86_64":
                codec_filename = "libopenh264.so"
            elif architecture in ["aarch64", "arm64"]:
                codec_filename = "libopenh264.so"
            else:
                codec_filename = "libopenh264.so"

            codec_path_h264 = os.path.join(self.model.app_path, "codecs", "openh264", codec_filename)
            codec_path_drm = "/opt/google/chrome/libwidevinecdmadapter.so"

        elif self.system == "windows":
            architecture = platform.machine()
            codec_filename = "openh264.dll"
            # if architecture == "AMD64":
            #     codec_filename = "openh264.dll"
            # else:
            #     codec_filename = "openh264.dll"

            codec_path_h264 = os.path.join(self.model.app_path, "codecs", "openh264", codec_filename)
            codec_path_drm = os.path.join(
                os.environ.get("PROGRAMFILES", ""),
                "Google",
                "Chrome",
                "Application",
                "WidevineCdm",
                "_platform_specific",
                "win_x64",
                "widevinecdm.dll",
            )

        elif self.system == "darwin":  # macOS
            codec_path_h264 = os.path.join(self.model.app_path, "codecs", "openh264", "libopenh264.dylib")
            codec_path_drm = "/Applications/Google Chrome.app/Contents/Versions/*/Google Chrome Framework.framework/Libraries/WidevineCdm/_platform_specific/mac_x64/widevinecdmadapter.plugin"

        else:
            raise Exception(f"Unsupported system: {system}")

        return codec_path_drm, codec_path_h264

    def _is_debug_mode(self):
        """Check if application is in debug mode."""
        return getattr(self, "debug_mode", False) or self.config.dikt.get("debug", False)

    def _configure_application_security(self):
        """Configure application-level security settings"""
        # Set application attributes for security
        if self.security_manager.os_type == OSType.WINDOWS:
            self.setAttribute(self.ApplicationAttribute.AA_DisableWindowContextHelpButton)

        # Log security configuration
        self._log_security_status()

    def _log_security_status(self):
        """Log the current security configuration"""
        config = self.security_manager.security_config

        print(f"Security Level: {config['security_level']}")
        print(f"OS: {config['os_type']} ({config['os_version']})")
        print(f"Environment: {config['environment']}")

        # Log warnings
        for warning in config["warnings"]:
            print(f"WARNING: {warning}")

        # Log capabilities
        capabilities = config["capabilities"]
        print(f"Process Isolation: {capabilities['process_isolation']}")
        print(f"Memory Protection: {capabilities['memory_protection']}")
        print(f"Network Sandbox: {capabilities['network_sandbox']}")


class NchantdMainWindow(pyqt.QMainWindow):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        super().__init__()
        self.config = condor.Instruct(pxcfg).select("NchantdMainWindow").addArgs(cfg)
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def closeEvent(self, event):
        """"""
        logma.info(f"Close {event}")
        # self.parent.model.auto_save()
        self.parent.model.maintain_application()
        return self

    def enterEvent(self, event):
        """"""
        # logma.info(f"Enter Event {event}")
        super().enterEvent(event)
        return self

    def focusInEvent(self, event):
        """"""
        logma.info(f"Focus In Event {event}")
        super().focusInEvent(event)
        return self

    def focusOutEvent(self, event):
        """"""
        logma.info(f"Focus Out Event {event}")
        super().focusOutEvent(event)
        return self

    def eventFilter(self, watched, event):
        """"""
        logma.info(f"Watched {watched} Event {event}")
        # Check if the application loses or gains focus
        logma.info(f"Type {event.type()}")
        if event.type() == pyqt.QEvent.ApplicationStateChange:
            app_state = pyqt.QApplication.instance().applicationState()
            logma.info(f"Application State {app_state}")
            if app_state == pyqt.Qt.ApplicationActive:
                # Application has regained focus, show the dialog again
                # self.dialog.show()
                # need to access all open dialogs
                pass
            else:
                # Application has lost focus, hide the dialog
                # self.dialog.hide()
                pass
        elif event.type() == event.WindowStateChange:
            state = self.windowState()
            if state == pyqt.Qt.WindowMinimized:  # The window was minimized.
                self.message_label.setText("Window State: Minimized")
            elif state == pyqt.Qt.WindowMaximized:
                self.message_label.setText("Window State: Maximized")
                print("The window was maximized.")
            elif state == pyqt.Qt.WindowNoState:
                self.message_label.setText("Window State: Normal")
                print("The window was restored to normal.")
        return super().eventFilter(watched, event)

    def hideEvent(self, event):
        """"""
        logma.info(f"Hide Event {event}")
        super().hideEvent(event)
        return self

    def keyPressEvent(self, event):
        """"""
        logma.info(f"Key Press Event {event}")
        super().keyPressEvent(event)
        return self

    def keyReleaseEvent(self, event):
        """"""
        logma.info(f"Key Release Event {event}")
        super().keyReleaseEvent(event)
        return self

    def leaveEvent(self, event):
        """"""
        # logma.info(f"Leave Event {event}")
        super().leaveEvent(event)
        return self

    def mouseDoubleClickEvent(self, event):
        """"""
        logma.info(f"Mouse Double Click Event {event}")
        super().mouseDoubleClickEvent(event)
        return self

    def mouseMoveEvent(self, event):
        """"""
        # logma.info(f"Mouse Move Event {event}")
        super().mouseMoveEvent(event)
        return self

    def mousePressEvent(self, event):
        """"""
        logma.info(f"Mouse Press Event {event}")
        super().mousePressEvent(event)
        return self

    def mouseReleaseEvent(self, event):
        """"""
        logma.info(f"Mouse Release Event {event}")
        super().mouseReleaseEvent(event)
        return self

    def moveEvent(self, event: pyqt.QMoveEvent):
        """"""
        logma.info(f"Application Moved  {event.pos()}")
        self.parent.view.on_window_move(event)
        return self

    def paintEvent(self, event):
        """"""
        # logma.info(f"Paint Event {event}")
        super().paintEvent(event)
        return self

    def resizeEvent(self, event: pyqt.QResizeEvent):
        """"""
        logma.info(f"Application Resized  {event.size()}")
        super().resizeEvent(event)
        return self

    def cmd_help(self):
        """"""
        pyqt.QMessageBox.information(self, "Help", "This is a help dialog displayed using Ctrl+H.")

    def cmd_save(self):
        """"""
        self.parent.model.save()

    def cmd_quit(self):
        """"""
        pyqt.QApplication.quit()

    def setup_shortcuts(self):
        """"""
        # Save shortcut
        save_shortcut = pyqt.QShortcut(pyqt.QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.cmd_save)

        # Quit shortcut
        quit_shortcut = pyqt.QShortcut(pyqt.QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.cmd_quit)

        # Help shortcut
        help_shortcut = pyqt.QShortcut(pyqt.QKeySequence("Ctrl+H"), self)
        help_shortcut.activated.connect(self.cmd_help)

    def showEvent(self, event):
        """"""


def detect_linux_display_system():
    """Detect the appropriate display system for Linux."""
    # Check environment variables first
    if environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    elif environ.get("DISPLAY"):
        return "x11"
    # Check for running display servers
    import subprocess

    try:
        # Check if Wayland is running
        result = subprocess.run(["pgrep", "-f", "wayland"], capture_output=True, text=True)
        if result.returncode == 0:
            return "wayland"

        # Check if X11 is running
        result = subprocess.run(["pgrep", "-f", "Xorg"], capture_output=True, text=True)
        if result.returncode == 0:
            return "x11"

    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Default fallback
    return "x11"


def diagnose_display_system():
    """Diagnose the current display system."""
    print("=== Display System Diagnostic ===")

    # Environment variables
    env_vars = [
        "DISPLAY",
        "WAYLAND_DISPLAY",
        "XDG_SESSION_TYPE",
        "XDG_CURRENT_DESKTOP",
        "DESKTOP_SESSION",
        "GDMSESSION",
    ]

    for var in env_vars:
        value = os.environ.get(var, "Not set")
        print(f"{var}: {value}")

    # Running processes
    import subprocess

    processes_to_check = [
        ("Xorg", "X11 server"),
        ("gnome-shell", "GNOME Shell"),
        ("kwin_wayland", "KDE Wayland"),
        ("sway", "Sway compositor"),
        ("weston", "Weston compositor"),
    ]

    for process, description in processes_to_check:
        try:
            result = subprocess.run(["pgrep", "-f", process], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {description} running (PID: {result.stdout.strip()})")
            else:
                print(f"✗ {description} not running")
        except FileNotFoundError:
            print(f"? Could not check {description} (pgrep not found)")


# ===========================Code Source Examples================================||
"""
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
