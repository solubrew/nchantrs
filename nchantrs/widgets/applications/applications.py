from typing import Any, List, Tuple, Union
"#\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n---  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n<(META)>: '3a0f63bb-96be-4c2f-bd5b-31fc64fd00b3' #\t\t\t\t\t\t\t\t||\n        docid:   #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        name: Nchantrs Module Nchantrs Python Excecution Document  #\t\t\t\t||\n        description: >  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n                Nchantrs allows for the modular creation of a gui app via  #\t\t\t||\n                configuration files.  The main window holds a grid of widgets such  #\t||\n                that each application is its own singular document type saving, new,  #\t||\n                open etc refers to the data used to populate the widgets.  The  #\t\t||\n                default data format for test_nchantrs applications is yaml files with the  #\t||\n                ability to override with an sql storage method  #\t\t\t\t\t\t||\n                leverage PyQt5TableModels to integrate tables\n        expirary: <[expiration]>  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        version: 0.0.0.0.0.0  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        authority: document|this  #\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        security: sec|lvl2  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n        <(WT)>: -32  #\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t||\n"
from os.path import abspath, dirname, exists, join, expanduser
from os import environ
from pathlib import Path
import os
from sys import argv
import platform
import logging
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.models.applicationmodels import NchantdCloakModel, NchantdPantiesModel
from nchantrs.library.nchantdlibrary import NchantdLibraryManager
from nchantrs.updates.db import NchantdDBUpdate
from nchantrs.views.applicationviews import NchantdCloakView, NchantdPantiesView
from nchantrs.widgets.controls.menus import NchantdContextMenu
from kahndor.logma import Logma
WINDOW_STATE_MESSAGES = {pyqt.Qt.WindowMinimized: 'Window State: Minimized', pyqt.Qt.WindowMaximized: 'Window State: Maximized', pyqt.Qt.WindowNoState: 'Window State: Normal'}
WINDOW_STATE_ACTIONS = {pyqt.Qt.WindowMaximized: lambda: logma.info('The window was maximized.'), pyqt.Qt.WindowNoState: lambda: logma.info('The window was restored to normal.')}
here = join(dirname(__file__), '')
logma = Logma(__name__)
log = False
if not log:
    logma.off()
debug = True
pxcfg = join(abspath(here), '_data_', 'applications.yaml')

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

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None, log_file=None) -> None:
        """
        Initializes an instance of the NchantdPanties class.

        :param name: The name of the instance.
        :type name: str
        :param parent: The parent instance.
        :type parent: NchantdPanties or None
        :param cfg: The configuration for the instance.
        :type cfg: dict or None
        :param log_file: Optional log file path for logging output.
        :type log_file: str or None
        """
        self.config = kahndor.Instruct(pxcfg).select('NchantdPanties').addArgs(args).override(cfg)
        logma.info(f"Panties Config {self.config.dikt.get('config', None)}")
        self.parent = parent
        self.application_name = name
        self.slug = self.application_name.lower().replace(' ', '_')
        super().__init__(argv)
        self.application_NCD = 'da1e9bb0-1dab-48de-ac28-9afa91568a39'
        self.dialogs = {}
        self.reset = None
        self.app = pyqt.QApplication.instance()
        self.model = NchantdPantiesModel(self, instance=instance)
        self.view = NchantdPantiesView(self)
        self.primary_focus = None
        self.is_installable = self.config.dikt.get('is_installable', False)
        self.is_install_optional = self.config.dikt.get('is_install_optional', False)
        self.is_install_selected = False
        if self.is_installable and self.is_install_optional is True:
            self.is_install_selected = self.config.dikt.get('is_install_selected', False)
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
        self.new_account = None
        self.startup = None
        self.recent_documents = []
        self.version = None
        self.context_menu = None

    def initApp(self, cfg=None) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def initModel(self, reset=None) -> Any:
        """
        :return:
        """
        if reset is not None:
            self.reset = reset
        self.model.initModel(self.reset)
        return self

    def initView(self, cfg=None) -> Any:
        """
        :return:
        """
        logma.info(f'Config {self.config.dikt}')
        self.view.initView(self.config.override(cfg))
        self.model.store.store_app_event('initialized', 'application view initialized')
        return self

    def initialize_configuration(self) -> None:
        logma.info(f'initialize_configuration called')
        return self

    def initialize_context_menu(self) -> Any:
        """"""
        cfg = {'actions': self.config.dikt.get('menus', {}).get('actions', [{'action': 'No Context', 'handler': None}])}
        self.context_menu = NchantdContextMenu(self, cfg).initWidget()
        return self

    def launch_dialog(self, dialog_name, name_override=None) -> Any:
        """"""
        name = dialog_name
        if name_override is not None:
            name = name_override
        self.dialogs[name] = get_dialog(dialog_name)
        self.dialogs[name](self, self.config)
        self.dialogs[name].initWidget()
        return self

    def __getstate__(self) -> Any:
        """"""
        state = self.__dict__.copy()
        if state.get('unpickable_attribute', False):
            del state['unpicklable_attribute']
        return state

    def __setstate__(self, state) -> None:
        """"""

class NchantdCloak(NchantdPanties):
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

    def __init__(self, name, instance=None, parent=None, cfg=None, args=None) -> None:
        """Initialize the application and the database then update all sink
        data tables from the established source endpoints"""
        super().__init__(name, instance, parent)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCloak').addArgs(args).override(cfg))
        self.main = NchantdMainWindow(self)
        self.model = NchantdCloakModel(self)
        self.view = NchantdCloakView(self)
        self.dbupdate = NchantdDBUpdate(self)

    def initApp(self, cfg=None) -> Any:
        """Initialize UI setting the main application layout and building
        landing widgets
        Load Pane based on the selection in the navigation tree"""
        self.system = platform.system().lower()
        self.set_version(self.config.dikt.get('config', {}).get('version', '0.0.1.0.1.0'))
        if self.has_agents is None:
            self.has_agents = self.config.dikt['config'].get('has_agents', False)
        self.agent_manager = None
        if self.has_comms is None:
            self.has_comms = self.config.dikt['config'].get('has_comms', False)
        self.comms_manager = None
        if self.has_services is None:
            self.has_services = self.config.dikt['config'].get('has_services', False)
        self.service_manager = None
        if self.has_extensions is None:
            self.has_extensions = self.config.dikt['config'].get('has_extensions', False)
        self.extension_manager = None
        if self.has_library is None:
            self.has_library = self.config.dikt['config'].get('has_library', False)
        self.library_manager = None
        self.init_managers()
        self.config.override(cfg)
        self.startup = self.config.dikt['startup']
        self.new_application = self.startup.new_application
        self.initModel()
        self.initView()
        pyqt.QTimer.singleShot(0, self.set_initial_state)
        try:
            self.exec_()
        except Exception as e:
            if self.has_comms:
                if self.comms_manager.notice_app_failed(e) == 'restart':
                    self.comms_manager.request_restart()
        return self

    def initModel(self, reset=None) -> Any:
        """"""
        super().initModel(reset)
        return self

    def initView(self) -> Any:
        """
        Initializes the view.

        :return: None
        """
        super().initView()
        self.main.setup_shortcuts()
        return self

    def init_managers(self) -> Any:
        """"""
        self.has_agents = False
        if self.has_agents:
            cfg = {}
            self.agent_manager = NchantdSentinelManager(self, cfg)
        if self.has_library:
            cfg = {}
            self.library_manager = NchantdLibraryManager(self, cfg)
        return self

    def get_current_version(self) -> Any:
        """"""
        return self.model.get_current_version()

    def run_on_launch(self) -> None:
        logma.info(f'run_on_launch called')
        return self

    def set_initial_state(self) -> Any:
        """"""
        self.run_on_launch()
        pane = self.view.panes['left'].tree
        pane.model.current_node.updateTabs('center')
        pane.model.current_node.updateTabs('right')
        pane.refresh()
        pyqt.QTimer.singleShot(500, self._select_home_node)
        return self

    def set_version(self, version) -> Any:
        """"""
        if version is None:
            version = '0.0.1.0.1.0'
        self.version = version
        return self

    def set_environment_variables(self, library_path) -> None:
        """Set environment variables for Chromium WebEngine."""
        if isinstance(library_path, str):
            library_path = Path(library_path)
        logma.info(f'Setting Environment Variables for Nchantd Office')
        logma.info(f'library_path: {library_path}')
        chromium_flags = self._build_chromium_flags(library_path)
        environ['QTWEBENGINE_CHROMIUM_FLAGS'] = ' '.join(chromium_flags)
        ozone_platform = detect_linux_display_system()
        logma.info(f'ozone_platform: {ozone_platform}')

    def _build_chromium_flags(self, library_path) -> List[Any]:
        """Build Chromium flags based on platform and configuration."""
        codec_path_drm, codec_path_h264 = self._get_codec_paths()
        cache_name = 'cache'
        base_flags = [f'--openh264-path={codec_path_h264}', '--enable-features=WebRTCUseH264', '--enable-features=RTCUseH264', '--force-fieldtrials=WebRTC-H264WithOpenH264FFmpeg/Enabled/', '--enable-accelerated-video-decode', '--enable-accelerated-mjpeg-decode', '--disable-features=UseChromeOSDirectVideoDecoder', '--enable-features=WebRTCHideLocalIpsWithMdns', '--enable-features=WebRTCAllowInputVolumeAdjustment', '--enable-webrtc-stun-origin', '--max-decoded-image-size-mb=512', '--enable-gpu-memory-buffer-video-frames', '--enable-zero-copy', '--enable-checker-imaging', f'--user-data-dir={self.model.app_path}/.persistence', f'--disk-cache-dir={self.model.app_path}/{cache_name}/Cache', f'--log-file={self.model.app_path}/logs/chromium.log', '--disable-dev-shm-usage', '--disable-gpu-process-for-dx12-vulkan-info-collection', '--disable-backgrounding-occluded-windows', '--disable-features=VizDisplayCompositor', '--disable-gpu-process-crash-limit', '--ignore-gpu-blocklist', '--disable-software-rasterizer']
        if debug:
            base_flags.extend(['--enable-logging=stderr', '--log-level=1', '--enable-features=LogJsConsoleMessages'])
        if self.system == 'linux':
            linux_flags = ['--enable-features=VaapiVideoDecoder,VaapiVideoEncoder,VaapiIgnoreDriverChecks', '--enable-hardware-overlays=single-fullscreen,single-on-top,underlay', '--enable-gpu-rasterization', '--disable-features=UseOzonePlatform', '--enable-features=PulseaudioLoopbackForCast,PulseaudioLoopbackForScreenShare', '--disable-seccomp-filter-sandbox' if self._needs_sandbox_relaxation() else '']
            base_flags.extend([f for f in linux_flags if f])
        elif self.system == 'windows':
            windows_flags = ['--enable-features=MediaFoundationH264Encoding', '--enable-win32k-renderer-lockdown', '--enable-features=D3D11VideoDecoder', '--disable-d3d11', '--enable-media-foundation-async-h264-encoding']
            base_flags.extend(windows_flags)
        elif self.system == 'darwin':
            macos_flags = ['--enable-features=VideoToolboxVP9Decoder', '--enable-videotoolbox-av1-decoding', '--disable-metal-test-shaders']
            base_flags.extend(macos_flags)
        return list(filter(None, list(dict.fromkeys(base_flags))))

    def _detect_display_system(self) -> Any:
        """Detect the appropriate display system for Linux."""
        if hasattr(self, '_display_system'):
            return self._display_system
        from os import environ
        if environ.get('WAYLAND_DISPLAY'):
            self._display_system = 'wayland'
        elif environ.get('DISPLAY'):
            self._display_system = 'x11'
        else:
            try:
                import subprocess
                result = subprocess.run(['pgrep', '-f', '(wayland|sway|weston)'], capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    self._display_system = 'wayland'
                else:
                    self._display_system = 'x11'
            except (subprocess.SubprocessError, FileNotFoundError, subprocess.TimeoutExpired):
                self._display_system = 'x11'
        #TODO implement method

    def _should_use_ozone(self) -> bool:
        """Determine if Ozone platform should be used."""
        display_system = self._detect_display_system()
        return display_system == 'wayland'

    def _needs_sandbox_relaxation(self) -> Union[Any, bool]:
        """Check if sandbox needs to be relaxed for codec access."""
        try:
            codec_path_drm, codec_path_h264 = self._get_codec_paths()
            return not os.access(codec_path_h264, os.R_OK)
        except Exception:
            return True

    def _get_codec_paths(self) -> Tuple[str, str]:
        """Get platform-specific codec paths for runtime-downloaded OpenH264."""
        if self.system == 'linux':
            architecture = platform.machine()
            if architecture == 'x86_64':
                codec_filename = 'libopenh264.so'
            elif architecture in ['aarch64', 'arm64']:
                codec_filename = 'libopenh264.so'
            else:
                codec_filename = 'libopenh264.so'
            codec_path_h264 = os.path.join(self.model.app_path, 'codecs', 'openh264', codec_filename)
            codec_path_drm = '/opt/google/chrome/libwidevinecdmadapter.so'
        elif self.system == 'windows':
            architecture = platform.machine()
            codec_filename = 'openh264.dll'
            codec_path_h264 = os.path.join(self.model.app_path, 'codecs', 'openh264', codec_filename)
            codec_path_drm = os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application', 'WidevineCdm', '_platform_specific', 'win_x64', 'widevinecdm.dll')
        elif self.system == 'darwin':
            codec_path_h264 = os.path.join(self.model.app_path, 'codecs', 'openh264', 'libopenh264.dylib')
            codec_path_drm = '/Applications/Google Chrome.app/Contents/Versions/*/Google Chrome Framework.framework/Libraries/WidevineCdm/_platform_specific/mac_x64/widevinecdmadapter.plugin'
        else:
            raise Exception(f'Unsupported system: {system}')
        return (codec_path_drm, codec_path_h264)

    def _is_debug_mode(self) -> Any:
        """Check if application is in debug mode."""
        return getattr(self, 'debug_mode', False) or self.config.dikt.get('debug', False)

    def _configure_application_security(self) -> None:
        """Configure application-level security settings"""
        if self.security_manager.os_type == OSType.WINDOWS:
            self.setAttribute(self.ApplicationAttribute.AA_DisableWindowContextHelpButton)
        self._log_security_status()

    def _log_security_status(self) -> None:
        """Log the current security configuration"""
        config = self.security_manager.security_config
        logma.critical(f"Security Level: {config['security_level']}")
        logma.critical(f"OS: {config['os_type']} ({config['os_version']})")
        logma.critical(f"Environment: {config['environment']}")
        for warning in config['warnings']:
            logma.warning(f'WARNING: {warning}')
        capabilities = config['capabilities']
        logma.critical(f"Process Isolation: {capabilities['process_isolation']}")
        logma.critical(f"Memory Protection: {capabilities['memory_protection']}")
        logma.critical(f"Network Sandbox: {capabilities['network_sandbox']}")

    def _select_home_node(self) -> Any:
        """Select the Home node after startup is complete"""
        logma.info('=== Selecting Home node after startup ===')
        try:
            tree = self.view.panes['left'].tree
            home_item = tree.topLevelItem(0)
            if home_item:
                tree.setCurrentItem(home_item)
                tree.scrollToItem(home_item)
                logma.info(f"Home node '{home_item.text(0)}' selected successfully")
            else:
                logma.error('Home node (topLevelItem 0) not found')
        except Exception as e:
            logma.error(f'Failed to select Home node: {e}')
        return self

class NchantdMainWindow(pyqt.QMainWindow):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        super().__init__()
        self.config = kahndor.Instruct(pxcfg).select('NchantdMainWindow').addArgs(cfg)
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def closeEvent(self, event) -> Any:
        """"""
        logma.info(f'Close {event}')
        self.parent.model.maintain_application()
        return self

    def enterEvent(self, event) -> Any:
        """"""
        super().enterEvent(event)
        return self

    def focusInEvent(self, event) -> Any:
        """"""
        logma.info(f'Focus In Event {event}')
        super().focusInEvent(event)
        return self

    def focusOutEvent(self, event) -> Any:
        """"""
        logma.info(f'Focus Out Event {event}')
        super().focusOutEvent(event)
        return self

    def eventFilter(self, watched, event) -> Any:
        """"""
        logma.info(f'Watched {watched} Event {event}')
        logma.info(f'Type {event.type()}')
        if event.type() == pyqt.QEvent.ApplicationStateChange:
            app_state = pyqt.QApplication.instance().applicationState()
            logma.info(f'Application State {app_state}')
            if app_state == pyqt.Qt.ApplicationActive:
                pass
            else:
                pass
        elif event.type() == event.WindowStateChange:
            state = self.windowState()
            message = WINDOW_STATE_MESSAGES.get(state, '')
            self.message_label.setText(message)
            action = WINDOW_STATE_ACTIONS.get(state)
            if action:
                action()
        return super().eventFilter(watched, event)

    def hideEvent(self, event) -> Any:
        """"""
        logma.info(f'Hide Event {event}')
        super().hideEvent(event)
        return self

    def keyPressEvent(self, event) -> Any:
        """"""
        logma.info(f'Key Press Event {event}')
        super().keyPressEvent(event)
        return self

    def keyReleaseEvent(self, event) -> Any:
        """"""
        logma.info(f'Key Release Event {event}')
        super().keyReleaseEvent(event)
        return self

    def leaveEvent(self, event) -> Any:
        """"""
        super().leaveEvent(event)
        return self

    def mouseDoubleClickEvent(self, event) -> Any:
        """"""
        logma.info(f'Mouse Double Click Event {event}')
        super().mouseDoubleClickEvent(event)
        return self

    def mouseMoveEvent(self, event) -> Any:
        """"""
        super().mouseMoveEvent(event)
        return self

    def mousePressEvent(self, event) -> Any:
        """"""
        logma.info(f'Mouse Press Event {event}')
        super().mousePressEvent(event)
        return self

    def mouseReleaseEvent(self, event) -> Any:
        """"""
        logma.info(f'Mouse Release Event {event}')
        super().mouseReleaseEvent(event)
        return self

    def moveEvent(self, event: pyqt.QMoveEvent) -> Any:
        """"""
        logma.info(f'Application Moved  {event.pos()}')
        self.parent.view.on_window_move(event)
        return self

    def paintEvent(self, event) -> Any:
        """"""
        super().paintEvent(event)
        return self

    def resizeEvent(self, event: pyqt.QResizeEvent) -> Any:
        """"""
        logma.info(f'Application Resized  {event.size()}')
        super().resizeEvent(event)
        return self

    def cmd_help(self) -> None:
        """"""
        pyqt.QMessageBox.information(self, 'Help', 'This is a help dialog displayed using Ctrl+H.')

    def cmd_save(self) -> None:
        """"""
        self.parent.model.save()

    def cmd_quit(self) -> None:
        """"""
        pyqt.QApplication.quit()

    def setup_shortcuts(self) -> None:
        """"""
        save_shortcut = pyqt.QShortcut(pyqt.QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.cmd_save)
        quit_shortcut = pyqt.QShortcut(pyqt.QKeySequence('Ctrl+Q'), self)
        quit_shortcut.activated.connect(self.cmd_quit)
        help_shortcut = pyqt.QShortcut(pyqt.QKeySequence('Ctrl+H'), self)
        help_shortcut.activated.connect(self.cmd_help)

    def showEvent(self, event) -> None:
        logma.info(f'showEvent called')
        return self

def detect_linux_display_system() -> str:
    """Detect the appropriate display system for Linux."""
    if environ.get('WAYLAND_DISPLAY'):
        return 'wayland'
    elif environ.get('DISPLAY'):
        return 'x11'
    import subprocess
    try:
        result = subprocess.run(['pgrep', '-f', 'wayland'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'wayland'
        result = subprocess.run(['pgrep', '-f', 'Xorg'], capture_output=True, text=True)
        if result.returncode == 0:
            return 'x11'
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    return 'x11'

def diagnose_display_system() -> None:
    """Diagnose the current display system."""
    logma.critical('=== Display System Diagnostic ===')
    env_vars = ['DISPLAY', 'WAYLAND_DISPLAY', 'XDG_SESSION_TYPE', 'XDG_CURRENT_DESKTOP', 'DESKTOP_SESSION', 'GDMSESSION']
    for var in env_vars:
        value = os.environ.get(var, 'Not set')
        logma.critical(f'{var}: {value}')
    import subprocess
    processes_to_check = [('Xorg', 'X11 server'), ('gnome-shell', 'GNOME Shell'), ('kwin_wayland', 'KDE Wayland'), ('sway', 'Sway compositor'), ('weston', 'Weston compositor')]
    for process, description in processes_to_check:
        try:
            result = subprocess.run(['pgrep', '-f', process], capture_output=True, text=True)
            if result.returncode == 0:
                logma.critical(f'{description} running (PID: {result.stdout.strip()}')
            else:
                logma.critical(f'{description} not running')
        except FileNotFoundError:
            logma.warning(f'Could not check {description} (pgrep not found)')
'\n'