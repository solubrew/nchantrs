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
from os import environ
import datetime as dt
import json as j
from enum import Enum
from typing import Dict, Optional
import uuid

import logging

logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from subtrix.subtrix import Mechanism
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.widgets import NchantdWidgetMixin

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
# logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "profiles.yaml")


class ProfileType(Enum):
    """Define different types of profiles"""

    DEFAULT = "default"
    SECURE = "secure"
    DEVELOPMENT = "development"
    INCOGNITO = "incognito"
    CUSTOM = "custom"


class NchantdWebProfile(NchantdWidgetMixin, pyqt.QWebEngineProfile):
    """"""

    def __init__(self, name, browser=None, intercept=False, parent=None, cfg=None):
        """ """
        super().__init__(name, browser)
        self.parent = parent
        self.name = name
        self.browser = browser
        self.config = kahndor.Instruct(pxcfg).select("NchantdWebProfile")
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.init_variables()
        logma.info(f"Initializing Web Profile {self.name}")
        # logma.info(f"Environment Variables: {environ["QTWEBENGINE_CHROMIUM_FLAGS"]}")
        # environ["QTWEBENGINE_CHROMIUM_FLAGS"] = " ".join(self.config.dikt["flags"].get("QTWEBENGINE_CHROMIUM_FLAGS"))
        self.type = None
        self.user = None
        self.intercept = intercept
        self.persistence = False

    def initProfile(self):
        """"""
        if self.intercept:
            self.initialize_interceptor()
        agent = self.config.dikt.get("agent", None)
        self.config.dikt["config"]["system-information"] = self.app.model.device.get_agent()
        self.config.dikt["config"]["webkit-version"] = self.config.dikt["config"]["webkit-version"][0]
        self.config.dikt["config"]["chrome-version"] = self.config.dikt["config"]["chrome-version"][0]
        self.config.dikt["config"]["safari-version"] = self.config.dikt["config"]["safari-version"][0]

        agent = agent.replace("<[system-information]>", str(self.config.dikt["config"]["system-information"]))
        agent = agent.replace("<[webkit-version]>", str(self.config.dikt["config"]["webkit-version"]))
        agent = agent.replace("<[chrome-version]>", str(self.config.dikt["config"]["chrome-version"]))
        agent = agent.replace("<[safari-version]>", str(self.config.dikt["config"]["safari-version"]))
        agent = agent.replace("<[CustomBrowser]>", str("NchantdBrowser"))
        agent = agent.replace("<[custom-version]>", str("0.0.1"))
        # agent = Mechanism(agent, self.config.dikt.get("config", {})).run()
        logma.info(agent)
        # raise Exception(f"Agent {agent}")

        self.setHttpUserAgent(agent)
        # self.setHttpCacheMaximumSize(0)
        self.initialize_settings()
        self.set_persistence()
        self.check_connection_security()
        return self

    def check_connection_security(self):
        """"""
        if not pyqt.QSslSocket.supportsSsl():
            raise RuntimeError("SSL support is required for secure communication.")
        return self

    def initialize_settings(self):
        """"""
        # settings = pyqt.QWebEngineSettings.globalSettings()
        settings = self.settings()
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptEnabled, True)  # Disable JavaScript
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)

        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)

        # Media-specific settings
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)

        if self.config.dikt["settings"].get("dns_prefetch", False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        if self.config.dikt["settings"].get("local_content_can_access_remote_urls", False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        if self.config.dikt["settings"].get("local_content_can_access_file_urls", False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        # settings.setAttribute(pyqt.QWebEngineSettings.LocalStorageEnabled, False)
        # self.current_profile.setHttpCacheType(pyqt.QWebEngineProfile.NoCache)
        if self.config.dikt["settings"].get("plugins", False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        if self.config.dikt["settings"].get("high_security", False):
            self.initialize_high_security(settings)
        self.initialize_gpu(settings)
        self.initialize_settings_drm(settings)
        return self

    def initialize_gpu(self, settings):
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        return self

    def initialize_high_security(self, settings):
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptEnabled, False)  # Disable JavaScript
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        return self

    def initialize_media(self, settings):
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AutoLoadMedia, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        return self

    def initialize_settings_drm(self, settings):
        """"""
        # ENABLE Protected Content using QWebEngineSettings
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        return self

    def initialize_interceptor(self):
        """"""
        logma.info(f"Initializing Interceptor {self.name}")
        interceptor = NchantdRequestInterceptor()
        self.defaultProfile().setUrlRequestInterceptor(interceptor)
        return self

    def load_local_storage(self):
        """"""
        return self

    def load_cache(self):
        """"""
        return self

    def set_persistence(self):
        """"""
        logma.info(f"Set Persistence {self.name}")
        # Use application path for storage
        storage_base = getattr(self.app.model.store, "application_path", ".")
        cache_path = join(storage_base, f".cache_{self.name}")
        persistent_path = join(storage_base, ".persistence", str(self.name))

        self.setCachePath(cache_path)
        self.setPersistentStoragePath(persistent_path)

        self.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)

        # Use a modern User-Agent for better compatibility (especially with Google)
        modern_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.setHttpUserAgent(modern_ua)

        self.persistence = True
        return self

    def set_persistent_storage_db(self, path):
        """"""
        return self

    def set_persistent_storage_path(self, path):
        """"""
        logma.info(f"Setting Persistent Storage Path: {path}")
        self.setPersistentStoragePath(path)
        return self

    def set_persistent_storage_type(self, type_="file"):
        """"""
        if type_ == "file":
            self.set_persistent_storage_path(self.app.model.path)
        elif type_ == "database":
            self.set_persistent_storage_db(self.app.model.path)
        return self

    def set_application_cache_storage(self):
        """"""
        return self

    def set_cache_storage(self):
        """"""
        return self

    def set_cookie_storage(self):
        """"""
        return self

    def set_file_system_api_storage(self):
        """"""
        return self

    def set_indexed_db_storage(self):
        """"""
        return self

    def set_local_storage(self):
        """"""
        return self

    def set_security_policy(self, policy_code="safe"):
        """"""
        # settings = pyqt.QWebEngineSettings.globalSettings()
        settings = self.settings()
        # The safest browsing possible that may in fact break things for use in highly sensitive interactions
        if policy_code == "safe":
            # ensure this is enabled via shell?
            #   QTWEBENGINE_DISABLE_SANDBOX=0
            # Disable Local Storage
            settings.setAttribute(pyqt.QWebEngineProfile.LocalStorageEnabled, False)
            self.setHttpUserAgent("SafeUserAgent")  # Customize user-agent
            # Prevent local files access
            settings.setAttribute(pyqt.QWebEngineSettings.LocalContentCanAccessFileUrls, False)
            # Prevent remote access
            settings.setAttribute(pyqt.QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
            settings.setAttribute(pyqt.QWebEngineSettings.JavascriptEnabled, False)  # Disable JavaScript
            settings.setAttribute(pyqt.QWebEngineSettings.LocalStorageEnabled, False)  # Block local storage
            settings.setAttribute(pyqt.QWebEngineSettings.PluginsEnabled, False)  # Disable plugins

        # Nearly Safe tries to strike a balance between being as safe as possible and not breaking much
        elif policy_code == "nearly_safe":
            pass

        # Mostly Safe is similar to any general browsing experience seeking to operate as safely as possibly without breaking anything
        elif policy_code == "mostly_safe":
            pass

        # Unsafe tries to run anything it can but will be transparent about potentially unafe things to the user
        elif policy_code == "unsafe":
            pass

        else:
            raise Exception(f"Invalid Security Policy Code {policy_code}")

        return self

    def set_service_worker_storage(self):
        """"""
        return self

    def set_session_storage(self):
        """"""
        return self

    def set_web_sql_storage(self):
        """"""
        return self

    def store_cache(self):
        """"""
        data = {"id": cache.id, "url": cache.url, "data": cache.data, "timestamp": cache.timestamp}
        payload = [Thing().uuid, self.user.app_profile_FK, "cache", j.dumps(data)]
        return self

    def store_cookie(self):
        """"""
        data = {
            "id": cookie.id,
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path,
            "expiration": cookie.expiration,
        }
        payload = [Thing().uuid, self.user.app_profile_FK, "cookie", j.dumps(data)]
        return self

    def store_indexed_db(self):
        """"""
        data = {"id": idb.id, "key": idb.key, "value": idb.value}
        payload = [Thing().uuid, self.user.app_profile_FK, "indexed_db", j.dumps(data)]
        return self

    def store_local_file(self):
        """"""
        data = {"id": local_file.id, "key": local_file.key, "value": local_file.value}
        payload = [Thing().uuid, self.user.app_profile_FK, "local_file", j.dumps(data)]
        return self

    def store_service_worker(self):
        data = {"id": service_worker.id, "scope": service_worker.scope, "script_url": service_worker.script_url}
        payload = [Thing().uuid, self.user.app_profile_FK, "service_worker", j.dumps(data)]
        return self

    def store_address(self):
        data = {"id": address.id, "chain_id": address.chain_id, "address": address.address}
        payload = [Thing().uuid, self.user.app_profile_FK, "address", j.dumps(data)]
        return self


class ProfileConfiguration:
    """Configuration class for web engine profiles"""

    def __init__(self, name: str, profile_type: ProfileType = ProfileType.DEFAULT):
        self.name = name
        self.profile_type = profile_type
        self.user_agent = "CustomBrowser/1.0"
        self.cache_enabled = True
        self.cookies_enabled = True
        self.javascript_enabled = True
        self.plugins_enabled = True
        self.storage_path = ""
        self.download_path = ""
        self.interceptor_rules = {}
        self.is_default = False

        # Apply type-specific defaults
        self._apply_type_defaults()

    def _apply_type_defaults(self):
        """Apply default settings based on profile type"""
        if self.profile_type == ProfileType.SECURE:
            self.interceptor_rules = {
                "blocked_domains": ["malicious-site.com", "tracking.com"],
                "blocked_extensions": [".exe", ".dll", ".bat"],
                "allowed_schemes": ["https"],
            }
            self.javascript_enabled = False
            self.plugins_enabled = False

        elif self.profile_type == ProfileType.DEVELOPMENT:
            self.user_agent = "DevBrowser/1.0 (Development)"
            self.interceptor_rules = {
                "blocked_domains": [],
                "blocked_extensions": [],
                "allowed_schemes": ["https", "http", "file", "data"],
            }

        elif self.profile_type == ProfileType.INCOGNITO:
            self.cache_enabled = False
            self.cookies_enabled = False
            self.storage_path = ""  # Off-the-record


class ProfileManager(pyqt.QObject):
    """Manages multiple web engine profiles"""

    profileCreated = pyqt.Signal(str, pyqt.QWebEngineProfile)  # profile_name, profile
    profileRemoved = pyqt.Signal(str)  # profile_name
    defaultProfileChanged = pyqt.Signal(str)  # profile_name

    def __init__(self, parent=None):
        super().__init__(parent)
        self.profiles: Dict[str, pyqt.QWebEngineProfile] = {}
        self.configurations: Dict[str, ProfileConfiguration] = {}
        self.interceptors: Dict[str, NchantdRequestInterceptor] = {}
        self.default_profile_name = "default"

        # Create default profile
        self.create_profile("default", ProfileType.DEFAULT, is_default=True)

    def create_profile(
        self,
        name: str,
        profile_type: ProfileType = ProfileType.DEFAULT,
        config: Optional[ProfileConfiguration] = None,
        is_default: bool = False,
    ) -> pyqt.QWebEngineProfile:
        """Create a new web engine profile"""

        if name in self.profiles:
            logma.warning(f"Profile '{name}' already exists")
            return self.profiles[name]

        # Create configuration if not provided
        if config is None:
            config = ProfileConfiguration(name, profile_type)
            config.is_default = is_default

        # Create the profile
        if profile_type == ProfileType.INCOGNITO:
            # Off-the-record profile
            profile = pyqt.QWebEngineProfile(self)
        else:
            # Persistent profile
            storage_name = f"profile_{name}_{uuid.uuid4().hex[:8]}"
            profile = pyqt.QWebEngineProfile(storage_name, self)

        # Configure the profile
        self._configure_profile(profile, config)

        # Store references
        self.profiles[name] = profile
        self.configurations[name] = config

        # Set as default if specified
        if is_default:
            self.set_default_profile(name)

        # Emit signal
        self.profileCreated.emit(name, profile)

        logma.info(f"Created profile '{name}' of type {profile_type.value}")
        return profile

    def _configure_profile(self, profile: pyqt.QWebEngineProfile, config: ProfileConfiguration):
        """Configure a profile with the given configuration"""

        # Basic settings
        profile.setHttpUserAgent(config.user_agent)

        # Cache settings
        if config.cache_enabled:
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        else:
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.NoCache)

        # Cookie settings
        if config.cookies_enabled:
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        else:
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)

        # Download path
        if config.download_path:
            profile.setDownloadPath(config.download_path)

        # Create and install request interceptor
        if config.interceptor_rules:
            interceptor = NchantdRequestInterceptor(config.name, config.interceptor_rules, profile)
            profile.setUrlRequestInterceptor(interceptor)
            self.interceptors[config.name] = interceptor

    def get_profile(self, name: str) -> Optional[pyqt.QWebEngineProfile]:
        """Get a profile by name"""
        return self.profiles.get(name)

    def get_default_profile(self) -> pyqt.QWebEngineProfile:
        """Get the default profile"""
        return self.profiles[self.default_profile_name]

    def set_default_profile(self, name: str):
        """Set a profile as default"""
        if name in self.profiles:
            old_default = self.default_profile_name
            self.default_profile_name = name

            # Update configurations
            if old_default in self.configurations:
                self.configurations[old_default].is_default = False
            self.configurations[name].is_default = True

            self.defaultProfileChanged.emit(name)
            logma.warning(f"Default profile changed to '{name}'")

    def remove_profile(self, name: str):
        """Remove a profile"""
        if name == self.default_profile_name:
            logma.warning(f"Cannot remove default profile '{name}'")
            return

        if name in self.profiles:
            # Clean up
            if name in self.interceptors:
                del self.interceptors[name]

            del self.profiles[name]
            del self.configurations[name]

            self.profileRemoved.emit(name)
            logger.info(f"Removed profile '{name}'")

    def get_profile_names(self) -> list:
        """Get list of all profile names"""
        return list(self.profiles.keys())

    def get_profile_info(self, name: str) -> Optional[Dict]:
        """Get profile information"""
        if name not in self.profiles:
            return None

        config = self.configurations[name]
        return {
            "name": name,
            "type": config.profile_type.value,
            "is_default": config.is_default,
            "cache_enabled": config.cache_enabled,
            "cookies_enabled": config.cookies_enabled,
            "user_agent": config.user_agent,
        }


# class SecureWebProfile(QWebEngineProfile):
#     """Security-enhanced web profile"""
#
#     def __init__(self, name: str, security_manager: CrossPlatformSecurityManager, parent=None):
#         super().__init__(name, parent)
#
#         self.security_manager = security_manager
#         self.security_config = security_manager.security_config
#
#         # Configure profile based on security assessment
#         self._configure_secure_profile()
#
#     def _configure_secure_profile(self):
#         """Configure profile with security settings"""
#
#         # Configure HTTP settings
#         self._configure_http_security()
#
#         # Configure web settings
#         self._configure_web_settings()
#
#         # Set up request interceptor
#         self._setup_request_interceptor()
#
#         # Configure storage settings
#         self._configure_storage_security()
#
#     def _configure_http_security(self):
#         """Configure HTTP-level security"""
#
#         # Set secure user agent
#         security_level = self.security_config["security_level"]
#
#         if security_level == "maximum":
#             # Minimal user agent for privacy
#             self.setHttpUserAgent("SecureBrowser/1.0")
#         else:
#             # Standard user agent with security identifier
#             self.setHttpUserAgent("SecureBrowser/1.0 (Security Enhanced)")
#
#         # Configure cache settings based on security level
#         if security_level in ["maximum", "high"]:
#             self.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
#             self.setHttpCacheMaximumSize(10 * 1024 * 1024)  # 10MB max
#         else:
#             self.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
#
#     def _configure_web_settings(self):
#         """Configure WebEngine settings based on security level"""
#         settings = self.settings()
#         security_level = self.security_config["security_level"]
#
#         # Base security settings for all levels
#         settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
#         settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
#         settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, False)
#
#         if security_level == "maximum":
#             # Maximum security: disable most features
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
#
#         elif security_level == "high":
#             # High security: selective feature enabling
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
#
#         else:
#             # Standard security: reasonable defaults
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
#             settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
#
#         # Platform-specific settings
#         self._apply_platform_specific_settings(settings)
#
#     def _apply_platform_specific_settings(self, settings):
#         """Apply platform-specific security settings"""
#
#         if self.security_manager.os_type == OSType.WINDOWS:
#             # Windows-specific security settings
#             if self.security_manager.capabilities.crypto_hardware:
#                 settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
#
#         elif self.security_manager.os_type == OSType.MACOS:
#             # macOS-specific settings
#             settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, False)
#
#         elif self.security_manager.os_type == OSType.LINUX:
#             # Linux-specific settings
#             if not self.security_manager.capabilities.process_isolation:
#                 # Additional restrictions when sandbox is disabled
#                 settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
#
#     def _setup_request_interceptor(self):
#         """Setup security-aware request interceptor"""
#         from security_request_interceptor import SecureRequestInterceptor
#
#         interceptor = SecureRequestInterceptor(self.security_manager)
#         self.setUrlRequestInterceptor(interceptor)
#
#     def _configure_storage_security(self):
#         """Configure storage settings based on security level"""
#         security_level = self.security_config["security_level"]
#
#         if security_level == "maximum":
#             # Maximum security: no persistent storage
#             self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
#
#         elif security_level == "high":
#             # High security: limited persistent storage
#             self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
#             # Set secure storage path
#             secure_path = self._get_secure_storage_path()
#             if secure_path:
#                 self.setPersistentStoragePath(secure_path)
#
#         else:
#             # Standard security: normal storage with restrictions
#             self.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
#
#     def _get_secure_storage_path(self) -> str:
#         """Get secure storage path based on platform"""
#         if self.security_manager.os_type == OSType.WINDOWS:
#             import os
#
#             return os.path.join(os.environ.get("LOCALAPPDATA", ""), "SecureBrowser")
#         elif self.security_manager.os_type == OSType.MACOS:
#             import os
#
#             return os.path.expanduser("~/Library/Application Support/SecureBrowser")
#         else:
#             import os
#
#             return os.path.expanduser("~/.local/share/SecureBrowser")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
