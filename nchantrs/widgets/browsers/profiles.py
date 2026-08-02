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
from os import environ
import datetime as dt
import json as j
import platform as _platform
from enum import Enum
from typing import Any, Dict, Optional
import uuid
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from subtrix.subtrix import Mechanism
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.browsers.requests import NchantdRequestInterceptor
from nchantrs.widgets.widgets import NchantdWidgetMixin
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', 'profiles.yaml')
_FALLBACK_CHROME_MAJOR = '138'

def _default_platform_token() -> str:
    """Return a UA platform token matching the host OS."""
    system = _platform.system()
    if system == 'Windows':
        return 'Windows NT 10.0; Win64; x64'
    if system == 'Darwin':
        return 'Macintosh; Intel Mac OS X 10_15_7'
    return 'X11; Linux x86_64'

def chromium_major_version() -> Any:
    """Major version of the Chromium that QtWebEngine is actually built on.

    Falls back to _FALLBACK_CHROME_MAJOR when the version API is unavailable
    (older bindings) or raises.
    """
    fn = getattr(pyqt, 'qWebEngineChromiumVersion', None)
    if fn is not None:
        try:
            version = fn()
            if version:
                return str(version).split('.')[0]
        except Exception:
            pass
    return _FALLBACK_CHROME_MAJOR

def modern_user_agent(platform_token=None) -> str:
    """Build a modern Chrome-compatible User-Agent string.

    The Chrome token tracks the real engine version so sites doing browser
    version checks (Gmail in particular) treat the view as current.

    NOTE (F2): advertising Chrome makes Google *hard-block* sign-in from this
    embedded QtWebEngine view ("this browser or app may not be secure"). The
    legacy non-Chrome UA (see DEFAULT_USER_AGENT) instead yields only a soft
    "unsupported browser" banner and still allows login. This helper is kept for
    non-Google contexts / future experiments but is NOT the current default.
    """
    if platform_token is None:
        platform_token = _default_platform_token()
    major = chromium_major_version()
    return f'Mozilla/5.0 ({platform_token}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major}.0.0.0 Safari/537.36'
_FIREFOX_VERSION = '140.0'

def firefox_user_agent(platform_token=None) -> str:
    """Build a current Firefox User-Agent string.

    Firefox is a *supported* Google browser, so it clears both the "unsupported
    browser" banner AND Google's embedded-Chrome hard block — provided the whole
    identity is consistently Firefox (profile UA, navigator, and client hints all
    align). We set this as the profile UA (not just a request-header rewrite) so
    Chromium does not emit contradicting Chrome ``Sec-CH-UA`` client hints. F2.
    """
    if platform_token is None:
        platform_token = _default_platform_token()
    return f'Mozilla/5.0 ({platform_token}; rv:{_FIREFOX_VERSION}) Gecko/20100101 Firefox/{_FIREFOX_VERSION}'
DEFAULT_USER_AGENT = firefox_user_agent()

def install_google_login_ua_script(profile) -> None:
    """Make ``navigator`` report Firefox on Google sign-in hosts.

    NchantdRequestInterceptor already rewrites the *request* User-Agent header to
    Firefox for those hosts, but Google's sign-in flow also reads the JS-visible
    ``navigator.userAgent`` / ``navigator.userAgentData``. If those still say
    Chrome, Google applies its embedded-Chrome integrity check and hard-blocks
    login ("this browser or app may not be secure"). This injects a main-world
    script (before page scripts) that overrides the navigator fields to Firefox
    values, but only when the page is on a Google sign-in host — everything else
    keeps the real Chrome navigator. See F2 / qutebrowser #5182.
    """
    try:
        from nchantrs.widgets.browsers.requests import ENABLE_GOOGLE_LOGIN_QUIRK, GOOGLE_LOGIN_HOSTS, google_login_user_agent
    except Exception as e:
        logma.error(f'[profiles] cannot load google login quirk: {e}')
        return
    if not ENABLE_GOOGLE_LOGIN_QUIRK:
        return
    ff_ua = google_login_user_agent()
    system = _platform.system()
    if system == 'Windows':
        platform_val, oscpu = ('Win32', 'Windows NT 10.0; Win64; x64')
    elif system == 'Darwin':
        platform_val, oscpu = ('MacIntel', 'Intel Mac OS X 10.15')
    else:
        platform_val, oscpu = ('Linux x86_64', 'Linux x86_64')
    hosts_js = ', '.join((j.dumps(h) for h in GOOGLE_LOGIN_HOSTS))
    js = f"\n(function() {{\n  try {{\n    var hosts = [{hosts_js}];\n    var h = (location.hostname || '').toLowerCase();\n    var match = hosts.some(function(x) {{ return h === x || h.endsWith('.' + x); }});\n    if (!match) return;\n    function def(prop, val) {{\n      try {{ Object.defineProperty(navigator, prop, {{get: function() {{ return val; }}, configurable: true}}); }} catch (e) {{}}\n    }}\n    def('userAgent', {j.dumps(ff_ua)});\n    def('appVersion', '5.0 (' + {j.dumps(platform_val)} + ')');\n    def('platform', {j.dumps(platform_val)});\n    def('oscpu', {j.dumps(oscpu)});\n    def('vendor', '');\n    def('vendorSub', '');\n    def('productSub', '20100101');\n    def('userAgentData', undefined);\n    // Chromium-only global that betrays a fake Firefox (real Firefox has no\n    // window.chrome). Hide it so the identity is consistently Firefox.\n    try {{ Object.defineProperty(window, 'chrome', {{get: function() {{ return undefined; }}, configurable: true}}); }} catch (e) {{}}\n  }} catch (e) {{}}\n}})();\n"
    try:
        script = pyqt.QWebEngineScript()
        script.setName('nchantd_google_login_uaquirk')
        script.setInjectionPoint(pyqt.QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(pyqt.QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(True)
        script.setSourceCode(js)
        collection = profile.scripts()
        already = any((s.name() == script.name() for s in collection.toList()))
        if not already:
            collection.insert(script)
    except Exception as e:
        logma.error(f'[profiles] could not insert google login quirk script: {e}')

class ProfileType(Enum):
    """Define different types of profiles"""
    DEFAULT = 'default'
    SECURE = 'secure'
    DEVELOPMENT = 'development'
    INCOGNITO = 'incognito'
    CUSTOM = 'custom'

class NchantdWebProfile(NchantdWidgetMixin, pyqt.QWebEngineProfile):
    """"""

    def __init__(self, name, browser=None, intercept=False, parent=None, cfg=None) -> None:
        """ """
        super().__init__(name, browser)
        self.parent = parent
        self.name = name
        self.browser = browser
        self.config = kahndor.Instruct(pxcfg).select('NchantdWebProfile').override(parent.config).override(cfg)
        self.init_variables()
        self.type = None
        self.user = None
        self.user_name = None
        self.user_email = None
        self.intercept = intercept
        self.persistence = False

    def initProfile(self) -> Any:
        """"""
        if self.intercept:
            self.initialize_interceptor()
        agent = self.config.dikt.get('agent', None)
        self.config.dikt['config']['system-information'] = self.app.model.device.get_agent()
        self.config.dikt['config']['webkit-version'] = self.config.dikt['config']['webkit-version'][0]
        self.config.dikt['config']['chrome-version'] = self.config.dikt['config']['chrome-version'][0]
        self.config.dikt['config']['safari-version'] = self.config.dikt['config']['safari-version'][0]
        agent = agent.replace('<[system-information]>', str(self.config.dikt['config']['system-information']))
        agent = agent.replace('<[webkit-version]>', str(self.config.dikt['config']['webkit-version']))
        agent = agent.replace('<[chrome-version]>', str(self.config.dikt['config']['chrome-version']))
        agent = agent.replace('<[safari-version]>', str(self.config.dikt['config']['safari-version']))
        agent = agent.replace('<[CustomBrowser]>', str('NchantdBrowser'))
        agent = agent.replace('<[custom-version]>', str('0.0.1'))
        logma.info(agent)
        self.setHttpUserAgent(agent)
        self.initialize_settings()
        self.set_persistence()
        self.check_connection_security()
        return self

    def check_connection_security(self) -> Any:
        """"""
        if not pyqt.QSslSocket.supportsSsl():
            raise RuntimeError('SSL support is required for secure communication.')
        return self

    def initialize_settings(self) -> Any:
        """"""
        settings = self.settings()
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowWindowActivationFromJavaScript, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.WebRTCPublicInterfacesOnly, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        if self.config.dikt['settings'].get('dns_prefetch', False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.DnsPrefetchEnabled, True)
        if self.config.dikt['settings'].get('local_content_can_access_remote_urls', False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        if self.config.dikt['settings'].get('local_content_can_access_file_urls', False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        if self.config.dikt['settings'].get('plugins', False):
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        if self.config.dikt['settings'].get('high_security', False):
            self.initialize_high_security(settings)
        self.initialize_gpu(settings)
        self.initialize_settings_drm(settings)
        return self

    def initialize_gpu(self, settings) -> Any:
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        return self

    def initialize_high_security(self, settings) -> Any:
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptEnabled, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        return self

    def initialize_media(self, settings) -> Any:
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AutoLoadMedia, False)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        return self

    def initialize_settings_drm(self, settings) -> Any:
        """"""
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.PlaybackRequiresUserGesture, True)
        settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        return self

    def initialize_interceptor(self) -> Any:
        """"""
        logma.info(f'Initializing Interceptor {self.name}')
        interceptor = NchantdRequestInterceptor()
        self.defaultProfile().setUrlRequestInterceptor(interceptor)
        return self

    def load_local_storage(self) -> Any:
        logma.info(f'load_local_storage called')
        return self

    def load_cache(self) -> Any:
        logma.info(f'load_cache called')
        return self

    def set_persistence(self) -> Any:
        """"""
        logma.info(f'Set Persistence {self.name}')
        storage_base = getattr(self.app.model.store, 'application_path', '.')
        cache_path = join(storage_base, f'.cache_{self.name}')
        persistent_path = join(storage_base, '.persistence', str(self.name))
        self.setCachePath(cache_path)
        self.setPersistentStoragePath(persistent_path)
        self.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        self.setHttpUserAgent(DEFAULT_USER_AGENT)
        self.setHttpAcceptLanguage('en-US,en;q=0.9')
        self.persistence = True
        return self

    def set_persistent_storage_db(self, path) -> Any:
        logma.info(f'set_persistent_storage_db called')
        if hasattr(self, 'persistent_storage_db'):
            logma.info(f'  has persistent_storage_db attr')
        return self

    def set_persistent_storage_path(self, path) -> Any:
        """"""
        logma.info(f'Setting Persistent Storage Path: {path}')
        self.setPersistentStoragePath(path)
        return self

    def set_persistent_storage_type(self, type_='file') -> Any:
        """"""
        if type_ == 'file':
            self.set_persistent_storage_path(self.app.model.path)
        elif type_ == 'database':
            self.set_persistent_storage_db(self.app.model.path)
        return self

    def set_application_cache_storage(self) -> Any:
        logma.info(f'set_application_cache_storage called')
        if hasattr(self, 'application_cache_storage'):
            logma.info(f'  has application_cache_storage attr')
        return self

    def set_cache_storage(self) -> Any:
        logma.info(f'set_cache_storage called')
        if hasattr(self, 'cache_storage'):
            logma.info(f'  has cache_storage attr')
        return self

    def set_cookie_storage(self) -> Any:
        logma.info(f'set_cookie_storage called')
        if hasattr(self, 'cookie_storage'):
            logma.info(f'  has cookie_storage attr')
        return self

    def set_file_system_api_storage(self) -> Any:
        logma.info(f'set_file_system_api_storage called')
        if hasattr(self, 'file_system_api_storage'):
            logma.info(f'  has file_system_api_storage attr')
        return self

    def set_indexed_db_storage(self) -> Any:
        logma.info(f'set_indexed_db_storage called')
        if hasattr(self, 'indexed_db_storage'):
            logma.info(f'  has indexed_db_storage attr')
        return self

    def set_local_storage(self) -> Any:
        logma.info(f'set_local_storage called')
        if hasattr(self, 'local_storage'):
            logma.info(f'  has local_storage attr')
        return self

    def set_security_policy(self, policy_code='safe') -> Any:
        """"""
        settings = self.settings()
        if policy_code == 'safe':
            settings.setAttribute(pyqt.QWebEngineProfile.LocalStorageEnabled, False)
            self.setHttpUserAgent(DEFAULT_USER_AGENT)
            settings.setAttribute(pyqt.QWebEngineSettings.LocalContentCanAccessFileUrls, False)
            settings.setAttribute(pyqt.QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
            settings.setAttribute(pyqt.QWebEngineSettings.JavascriptEnabled, False)
            settings.setAttribute(pyqt.QWebEngineSettings.LocalStorageEnabled, False)
            settings.setAttribute(pyqt.QWebEngineSettings.PluginsEnabled, False)
        elif policy_code == 'nearly_safe':
            pass
        elif policy_code == 'mostly_safe':
            pass
        elif policy_code == 'unsafe':
            pass
        else:
            raise Exception(f'Invalid Security Policy Code {policy_code}')
        return self

    def set_service_worker_storage(self) -> Any:
        logma.info(f'set_service_worker_storage called')
        if hasattr(self, 'service_worker_storage'):
            logma.info(f'  has service_worker_storage attr')
        return self

    def set_session_storage(self) -> Any:
        logma.info(f'set_session_storage called')
        if hasattr(self, 'session_storage'):
            logma.info(f'  has session_storage attr')
        return self

    def set_web_sql_storage(self) -> Any:
        logma.info(f'set_web_sql_storage called')
        if hasattr(self, 'web_sql_storage'):
            logma.info(f'  has web_sql_storage attr')
        return self

    def store_cache(self) -> Any:
        """"""
        data = {'id': cache.id, 'url': cache.url, 'data': cache.data, 'timestamp': cache.timestamp}
        payload = [Thing().uuid, self.user.app_profile_FK, 'cache', j.dumps(data)]
        return self

    def store_cookie(self) -> Any:
        """"""
        data = {'id': cookie.id, 'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path, 'expiration': cookie.expiration}
        payload = [Thing().uuid, self.user.app_profile_FK, 'cookie', j.dumps(data)]
        return self

    def store_indexed_db(self) -> Any:
        """"""
        data = {'id': idb.id, 'key': idb.key, 'value': idb.value}
        payload = [Thing().uuid, self.user.app_profile_FK, 'indexed_db', j.dumps(data)]
        return self

    def store_local_file(self) -> Any:
        """"""
        data = {'id': local_file.id, 'key': local_file.key, 'value': local_file.value}
        payload = [Thing().uuid, self.user.app_profile_FK, 'local_file', j.dumps(data)]
        return self

    def store_service_worker(self) -> Any:
        data = {'id': service_worker.id, 'scope': service_worker.scope, 'script_url': service_worker.script_url}
        payload = [Thing().uuid, self.user.app_profile_FK, 'service_worker', j.dumps(data)]
        return self

    def store_address(self) -> Any:
        data = {'id': address.id, 'chain_id': address.chain_id, 'address': address.address}
        payload = [Thing().uuid, self.user.app_profile_FK, 'address', j.dumps(data)]
        return self

class ProfileConfiguration:
    """Configuration class for web engine profiles"""

    def __init__(self, name: str, profile_type: ProfileType=ProfileType.DEFAULT) -> None:
        self.name = name
        self.profile_type = profile_type
        self.user_agent = DEFAULT_USER_AGENT
        self.cache_enabled = True
        self.cookies_enabled = True
        self.javascript_enabled = True
        self.plugins_enabled = True
        self.storage_path = ''
        self.download_path = ''
        self.interceptor_rules = {}
        self.is_default = False
        self._apply_type_defaults()

    def _apply_type_defaults(self) -> None:
        """Apply default settings based on profile type"""
        if self.profile_type == ProfileType.SECURE:
            self.interceptor_rules = {'blocked_domains': ['malicious-site.com', 'tracking.com'], 'blocked_extensions': ['.exe', '.dll', '.bat'], 'allowed_schemes': ['https']}
            self.javascript_enabled = False
            self.plugins_enabled = False
        elif self.profile_type == ProfileType.DEVELOPMENT:
            self.user_agent = DEFAULT_USER_AGENT
            self.interceptor_rules = {'blocked_domains': [], 'blocked_extensions': [], 'allowed_schemes': ['https', 'http', 'file', 'data']}
        elif self.profile_type == ProfileType.INCOGNITO:
            self.cache_enabled = False
            self.cookies_enabled = False
            self.storage_path = ''

class ProfileManager(pyqt.QObject):
    """Manages multiple web engine profiles"""
    profileCreated = pyqt.Signal(str, pyqt.QWebEngineProfile)
    profileRemoved = pyqt.Signal(str)
    defaultProfileChanged = pyqt.Signal(str)

    def __init__(self, parent=None, storage_base=None) -> None:
        super().__init__(parent)
        self.profiles: Dict[str, pyqt.QWebEngineProfile] = {}
        self.configurations: Dict[str, ProfileConfiguration] = {}
        self.interceptors: Dict[str, NchantdRequestInterceptor] = {}
        self.default_profile_name = 'default'
        self.storage_base = storage_base or '.'
        logma.info(f'[profiles] ProfileManager init | storage_base={self.storage_base!r}')
        self.create_profile('default', ProfileType.DEFAULT, is_default=True)

    def get_or_create(self, name: str, profile_type: 'ProfileType'=None) -> pyqt.QWebEngineProfile:
        """Return an existing profile or create a persistent one with this name."""
        if name in self.profiles:
            return self.profiles[name]
        return self.create_profile(name, profile_type or ProfileType.DEFAULT)

    def create_profile(self, name: str, profile_type: ProfileType=ProfileType.DEFAULT, config: Optional[ProfileConfiguration]=None, is_default: bool=False) -> pyqt.QWebEngineProfile:
        """Create a new web engine profile"""
        if name in self.profiles:
            logma.warning(f"Profile '{name}' already exists")
            return self.profiles[name]
        if config is None:
            config = ProfileConfiguration(name, profile_type)
            config.is_default = is_default
        if profile_type == ProfileType.INCOGNITO:
            profile = pyqt.QWebEngineProfile(self)
        else:
            storage_name = f'profile_{name}'
            profile = pyqt.QWebEngineProfile(storage_name, self)
        self._configure_profile(profile, config)
        self.profiles[name] = profile
        self.configurations[name] = config
        if is_default:
            self.set_default_profile(name)
        self.profileCreated.emit(name, profile)
        logma.info(f"Created profile '{name}' of type {profile_type.value}")
        return profile

    def _configure_profile(self, profile: pyqt.QWebEngineProfile, config: ProfileConfiguration) -> None:
        """Configure a profile with the given configuration"""
        from os import makedirs
        profile.setHttpUserAgent(config.user_agent)
        profile.setHttpAcceptLanguage('en-US,en;q=0.9')
        try:
            settings = profile.settings()
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptEnabled, config.javascript_enabled)
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(pyqt.QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        except Exception as e:
            logma.error(f"[profiles] could not apply web settings for '{config.name}': {e}")
        install_google_login_ua_script(profile)
        if config.profile_type != ProfileType.INCOGNITO and (not profile.isOffTheRecord()):
            persistent_path = config.storage_path or join(self.storage_base, '.webprofiles', config.name)
            cache_path = join(self.storage_base, '.webprofiles', config.name, 'cache')
            try:
                makedirs(persistent_path, exist_ok=True)
                makedirs(cache_path, exist_ok=True)
            except Exception as e:
                logma.error(f"[profiles] could not create profile dirs for '{config.name}': {e}")
            profile.setPersistentStoragePath(persistent_path)
            profile.setCachePath(cache_path)
        if config.cache_enabled:
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.DiskHttpCache)
        else:
            profile.setHttpCacheType(pyqt.QWebEngineProfile.HttpCacheType.NoCache)
        if config.cookies_enabled:
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        else:
            profile.setPersistentCookiesPolicy(pyqt.QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies)
        if config.download_path:
            profile.setDownloadPath(config.download_path)
        if config.name not in self.interceptors:
            try:
                if config.interceptor_rules:
                    interceptor = NchantdRequestInterceptor(config.name, config.interceptor_rules, profile)
                else:
                    interceptor = NchantdRequestInterceptor(profile)
                profile.setUrlRequestInterceptor(interceptor)
                self.interceptors[config.name] = interceptor
            except Exception as e:
                logma.error(f"[profiles] could not install interceptor for '{config.name}': {e}")
        logma.info(f"[profiles] configured '{config.name}' | off_the_record={profile.isOffTheRecord()} | storage={profile.persistentStoragePath()!r} | cache={profile.cachePath()!r} | cache_type={profile.httpCacheType()} | cookies={profile.persistentCookiesPolicy()}")

    def get_profile(self, name: str) -> Optional[pyqt.QWebEngineProfile]:
        """Get a profile by name"""
        return self.profiles.get(name)

    def get_default_profile(self) -> pyqt.QWebEngineProfile:
        """Get the default profile"""
        return self.profiles[self.default_profile_name]

    def set_default_profile(self, name: str) -> None:
        """Set a profile as default"""
        if name in self.profiles:
            old_default = self.default_profile_name
            self.default_profile_name = name
            if old_default in self.configurations:
                self.configurations[old_default].is_default = False
            self.configurations[name].is_default = True
            self.defaultProfileChanged.emit(name)
            logma.warning(f"Default profile changed to '{name}'")

    def remove_profile(self, name: str) -> None:
        """Remove a profile"""
        if name == self.default_profile_name:
            logma.warning(f"Cannot remove default profile '{name}'")
            return
        if name in self.profiles:
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
        return {'name': name, 'type': config.profile_type.value, 'is_default': config.is_default, 'cache_enabled': config.cache_enabled, 'cookies_enabled': config.cookies_enabled, 'user_agent': config.user_agent}