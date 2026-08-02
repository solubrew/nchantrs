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
import datetime as dt
import enum
import dataclasses
import platform as _platform
from typing import Optional
import logging
from collections.abc import Callable
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from nchantrs.widgets.browsers.utilities import NchantdURL
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)
if not log:
    logma.off()
pxcfg = join(here, '_data_', '.yaml')
ENABLE_GOOGLE_LOGIN_QUIRK = True
_FIREFOX_VERSION = '140.0'
GOOGLE_LOGIN_HOSTS = ('accounts.google.com', 'accounts.youtube.com')

def _quirk_platform_token() -> str:
    """UA platform token for the host OS, in Firefox's format."""
    system = _platform.system()
    if system == 'Windows':
        return 'Windows NT 10.0; Win64; x64'
    if system == 'Darwin':
        return 'Macintosh; Intel Mac OS X 10.15'
    return 'X11; Linux x86_64'

def google_login_user_agent() -> str:
    """Firefox User-Agent used on Google sign-in hosts (F2 quirk)."""
    return f'Mozilla/5.0 ({_quirk_platform_token()}; rv:{_FIREFOX_VERSION}) Gecko/20100101 Firefox/{_FIREFOX_VERSION}'

def is_google_login_host(host) -> bool:
    """True if host is (or is under) a Google sign-in host."""
    host = (host or '').lower()
    return any((host == h or host.endswith('.' + h) for h in GOOGLE_LOGIN_HOSTS))

class NchantdLocalServiceRequestInterceptor(pyqt.QWebEngineUrlRequestInterceptor):
    """Request interceptor optimized for local services"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.local_hosts = {'localhost', '127.0.0.1', '0.0.0.0'}

    def interceptRequest(self, info) -> None:
        """Intercept requests and handle local service specifics"""
        url = info.requestUrl()
        host = url.host().lower()
        if host in self.local_hosts:
            logma.info(f'Local service request: {url.toString()}')
            headers = info.requestHeaders()
            headers['X-Requested-With'] = b'LocalBrowser'
            headers['X-Local-Development'] = b'true'
            info.setRequestHeaders(headers)

class NchantdRequestInterceptor(pyqt.QWebEngineUrlRequestInterceptor):
    """"""
    BLOCK_JAVASCRIPT = True
    RULES = [{'type': 'deny_domain', 'value': 'malicious-site.com'}, {'type': 'deny_extension', 'value': '.exe'}, {'type': 'allow_only_domain', 'value': 'https://safe-site.com'}]

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    def interceptRequest(self, info) -> None:
        """Diagnostic logging only (no blocking).

        Logs every resource request — including XHR/fetch and WebSocket handshakes
        — so we can see which request the Jupyter front-end is failing on
        ("Failed to fetch"). Especially flags /api/ and websocket requests.
        """
        try:
            url = info.requestUrl().toString()
            method = bytes(info.requestMethod()).decode('ascii', 'replace')
            rtype = info.resourceType()
            fp = info.firstPartyUrl().toString()
            is_api = '/api/' in url
            is_ws = url.startswith('ws://') or url.startswith('wss://')
            if is_api or is_ws:
                logma.info(f'[req] {method} {url} | type={rtype} | api={is_api} ws={is_ws} | firstParty={fp}')
            else:
                logma.info(f'[req] {method} {url} | type={rtype}')
        except Exception as e:
            logma.error(f'[req] interceptor log failed: {e}')
        try:
            if ENABLE_GOOGLE_LOGIN_QUIRK and is_google_login_host(info.requestUrl().host()):
                info.setHttpHeader(b'User-Agent', google_login_user_agent().encode('ascii'))
        except Exception as e:
            logma.error(f'[req] google login UA quirk failed: {e}')
        return

    def intercept_media(self) -> None:
        logma.info(f'intercept_media called')
        return self

    def _block_javascript(self, info) -> None:
        """"""
        if info.requestUrl().toString().endswith('.js'):
            logma.info(f'Blocking external script: {info.requestUrl().toString()}')
            info.block(True)

    def _check_allow(self) -> None:
        """"""

    def _setup_security_rules(self) -> None:
        """Setup security rules based on security level"""
        self.security_level = 'low'
        if self.security_level == 'low':
            return
        self.blocked_domains = set()
        self.blocked_extensions = set()
        self.allowed_schemes = {'https', 'data'}
        if self.security_level == 'maximum':
            self.blocked_extensions.update({'.exe', '.dll', '.bat', '.cmd', '.scr'})
            self.allowed_schemes = {'https'}
        elif self.security_level == 'high':
            self.blocked_extensions.update({'.exe', '.dll', '.bat', '.cmd'})
            self.allowed_schemes.update({'http'})
        self.blocked_domains.update({'malicious-site.com', 'suspicious-domain.net'})

    def _apply_maximum_security_filters(self, info) -> None:
        """Apply maximum security filtering"""
        url_string = info.requestUrl().toString()
        if url_string.endswith('.js'):
            logma.info(f'Blocked JavaScript file in maximum security mode: {url_string}')
            info.block(True)
            return
        tracking_patterns = ['analytics', 'tracking', 'ads', 'facebook', 'google-analytics']
        if any((pattern in url_string.lower() for pattern in tracking_patterns)):
            logma.info(f'Blocked tracking request: {url_string}')
            info.block(True)
            return

    def _apply_high_security_filters(self, info) -> None:
        """Apply high security filtering"""
        url_string = info.requestUrl().toString()
        ad_patterns = ['/ads/', '/ad/', 'doubleclick', 'googlesyndication']
        if any((pattern in url_string.lower() for pattern in ad_patterns)):
            logma.info(f'Blocked advertising request: {url_string}')
            info.block(True)
            return

class ResourceType(enum.Enum):
    """Possible request types that can be received.

    Currently corresponds to the QWebEngineUrlRequestInfo Enum:
    https://doc.qt.io/qt-6/qwebengineurlrequestinfo.html#ResourceType-enum
    """
    main_frame = 0
    sub_frame = 1
    stylesheet = 2
    script = 3
    image = 4
    font_resource = 5
    sub_resource = 6
    object = 7
    media = 8
    worker = 9
    shared_worker = 10
    prefetch = 11
    favicon = 12
    xhr = 13
    ping = 14
    service_worker = 15
    csp_report = 16
    plugin_resource = 17
    preload_main_frame = 19
    preload_sub_frame = 20
    json = 21
    websocket = 254
    unknown = 255

class RedirectException(Exception):
    """Raised when the request was invalid, or a request was already made."""

@dataclasses.dataclass
class NchantdRequest:
    """A request which can be intercepted/blocked."""
    first_party_url: Optional[NchantdURL]
    request_url: NchantdURL
    is_blocked: bool = False
    resource_type: Optional[ResourceType] = None

    def block(self) -> None:
        """Block this request."""
        self.is_blocked = True

    def redirect(self, url: NchantdURL, *, ignore_unsupported: bool=False) -> None:
        """Redirect this request.

        Only some types of requests can be successfully redirected.
        Improper use of this method can result in redirect loops.

        This method will throw a RedirectException if the request was not possible.

        Args:
            url: The QUrl to try to redirect to.
            ignore_unsupported: If set to True, request methods which can't be
                redirected (such as POST) are silently ignored instead of throwing an
                exception.
        """
        raise NotImplementedError

class CloudflareHandler(pyqt.QWebEngineView):
    """Handler for Cloudflare challenges"""
    challenge_detected = pyqt.Signal()
    challenge_completed = pyqt.Signal()
    challenge_failed = pyqt.Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.challenge_timer = QTimer()
        self.challenge_timer.timeout.connect(self.check_challenge_status)
        self.page().loadFinished.connect(self.on_load_finished)
        logma.info(f'CloudflareHandler initialized')

    def on_load_finished(self, success) -> None:
        """Check for Cloudflare challenge after page load"""
        if success:
            self.detect_cloudflare_challenge()

    def detect_cloudflare_challenge(self) -> None:
        """Detect if a Cloudflare challenge is present"""
        js_code = '\n        (function() {\n            // Check for various Cloudflare challenge indicators\n            const challengeSelectors = [\n                \'.cf-browser-verification\',\n                \'.cf-checking-browser\',\n                \'[data-sitekey]\',\n                \'#challenge-form\',\n                \'.challenge-container\',\n                \'input[name="cf_captcha_kind"]\'\n            ];\n\n            let challengeFound = false;\n            let challengeType = null;\n\n            for (const selector of challengeSelectors) {\n                const element = document.querySelector(selector);\n                if (element) {\n                    challengeFound = true;\n                    challengeType = selector;\n                    break;\n                }\n            }\n\n            // Check for Turnstile widget specifically\n            const turnstileWidget = document.querySelector(\'[data-sitekey]\');\n            const isTurnstile = turnstileWidget !== null;\n\n            return {\n                challenge_detected: challengeFound,\n                challenge_type: challengeType,\n                is_turnstile: isTurnstile,\n                page_title: document.title,\n                url: window.location.href,\n                ready_state: document.readyState\n            };\n        })();\n        '
        self.page().runJavaScript(js_code, self.handle_challenge_detection)

    def handle_challenge_detection(self, result) -> None:
        """Handle challenge detection result"""
        if result and result.get('challenge_detected'):
            logger.info(f"Cloudflare challenge detected: {result.get('challenge_type')}")
            self.challenge_detected.emit()
            self.challenge_timer.start(1000)
            if result.get('is_turnstile'):
                self.help_turnstile_render()
        else:
            logger.debug('No Cloudflare challenge detected')

    def help_turnstile_render(self) -> None:
        """Help Turnstile widget render properly"""
        js_code = "\n        (function() {\n            // Force Turnstile to re-initialize\n            if (window.turnstile && window.turnstile.render) {\n                const widgets = document.querySelectorAll('[data-sitekey]');\n                widgets.forEach(function(widget, index) {\n                    if (!widget.innerHTML.trim()) {\n                        try {\n                            const sitekey = widget.getAttribute('data-sitekey');\n                            if (sitekey) {\n                                window.turnstile.render(widget, {\n                                    sitekey: sitekey,\n                                    callback: function(token) {\n                                        console.log('Turnstile completed:', token);\n                                    }\n                                });\n                            }\n                        } catch (e) {\n                            console.log('Turnstile render error:', e);\n                        }\n                    }\n                });\n            }\n\n            // Also try triggering resize events which can help with rendering\n            window.dispatchEvent(new Event('resize'));\n\n            return {\n                turnstile_available: typeof window.turnstile !== 'undefined',\n                widgets_found: document.querySelectorAll('[data-sitekey]').length\n            };\n        })();\n        "
        self.page().runJavaScript(js_code, lambda result: logger.debug('Turnstile help result: %s', result))

    def check_challenge_status(self) -> None:
        """Periodically check if challenge is completed"""
        js_code = '\n        (function() {\n            // Check if we\'re still on a challenge page\n            const challengeSelectors = [\n                \'.cf-browser-verification\',\n                \'.cf-checking-browser\',\n                \'#challenge-form\'\n            ];\n\n            let stillChallenging = false;\n            for (const selector of challengeSelectors) {\n                if (document.querySelector(selector)) {\n                    stillChallenging = true;\n                    break;\n                }\n            }\n\n            // Check if Turnstile is completed\n            const turnstileCompleted = document.querySelector(\'input[name="cf-turnstile-response"]\')?.value || false;\n\n            return {\n                still_challenging: stillChallenging,\n                turnstile_completed: !!turnstileCompleted,\n                current_url: window.location.href,\n                page_title: document.title\n            };\n        })();\n        '
        self.page().runJavaScript(js_code, self.handle_challenge_status)

    def handle_challenge_status(self, result) -> None:
        """Handle challenge status check"""
        if result:
            if not result.get('still_challenging') and result.get('turnstile_completed'):
                logger.info('Cloudflare challenge completed!')
                self.challenge_timer.stop()
                self.challenge_completed.emit()