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
import enum
import dataclasses
from typing import Optional

import logging
from collections.abc import Callable

logger = logging.getLogger(__name__)

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
from nchantrs.widgets.browsers.utilities import NchantdURL

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)


# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdLocalServiceRequestInterceptor(pyqt.QWebEngineUrlRequestInterceptor):
    """Request interceptor optimized for local services"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.local_hosts = {"localhost", "127.0.0.1", "0.0.0.0"}

    def interceptRequest(self, info):
        """Intercept requests and handle local service specifics"""
        url = info.requestUrl()
        host = url.host().lower()
        # Log local service requests
        if host in self.local_hosts:
            logma.info(f"Local service request: {url.toString()}")
            # Add development headers for local services
            headers = info.requestHeaders()
            headers["X-Requested-With"] = b"LocalBrowser"
            headers["X-Local-Development"] = b"true"
            info.setRequestHeaders(headers)


class NchantdRequestInterceptor(pyqt.QWebEngineUrlRequestInterceptor):
    """"""

    BLOCK_JAVASCRIPT = True
    RULES = [
        {"type": "deny_domain", "value": "malicious-site.com"},
        {"type": "deny_extension", "value": ".exe"},
        {"type": "allow_only_domain", "value": "https://safe-site.com"},
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

    def interceptRequest(self, info):
        """"""
        # profile = info.profile()
        # # data = profile.property("custom-data")
        # logma.info(profile.url().toString())
        # logma.info(f"URL Request intercepted: {info.requestUrl().toString()}")
        # logma.info(f"Request Method: {info.requestMethod()}")
        # # for header, value in info.requestHeaders().items():
        # #     logma.info(f"Request Header: {header} - {value}")
        #
        # self._setup_security_rules()
        # url = info.requestUrl()
        # url_string = url.toString()
        #
        # # Log request for security monitoring
        # logma.info(f"Request intercepted: {url_string}")
        #
        # if self.security_level in ("maximum", "high"):
        #     # Check URL scheme
        #     if url.scheme() not in self.allowed_schemes:
        #         logma.info(f"Blocked request with disallowed scheme: {url.scheme()}")
        #         info.block(True)
        #         return
        #     # Check for blocked domains
        #     host = url.host().lower()
        #     if host in self.blocked_domains:
        #         logma.info(f"Blocked request to suspicious domain: {host}")
        #         info.block(True)
        #         return
        #     # Check for blocked file extensions
        #     path = url.path().lower()
        #     for ext in self.blocked_extensions:
        #         if path.endswith(ext):
        #             logma.info(f"Blocked request for dangerous file: {path}")
        #             info.block(True)
        #             return
        #     if self.BLOCK_JAVASCRIPT == True:
        #         self._block_javascript(info)
        #     # Security level specific filtering
        #     if self.security_level == "maximum":
        #         self._apply_maximum_security_filters(info)
        #     elif self.security_level == "high":
        #         self._apply_high_security_filters(info)

    def intercept_media(self):
        """"""

    def _block_javascript(self, info):
        """"""
        if info.requestUrl().toString().endswith(".js"):
            logma.info(f"Blocking external script: {info.requestUrl().toString()}")
            info.block(True)

    def _check_allow(self):
        """"""

    def _setup_security_rules(self):
        """Setup security rules based on security level"""
        # self.security_manager = CrossPlatformSecurityManager()
        # self.security_level = security_manager.security_config["security_level"]
        self.security_level = "low"
        if self.security_level == "low":
            return
        self.blocked_domains = set()
        self.blocked_extensions = set()
        self.allowed_schemes = {"https", "data"}

        if self.security_level == "maximum":
            # Maximum security: very restrictive
            self.blocked_extensions.update({".exe", ".dll", ".bat", ".cmd", ".scr"})
            self.allowed_schemes = {"https"}  # Only HTTPS

        elif self.security_level == "high":
            # High security: moderately restrictive
            self.blocked_extensions.update({".exe", ".dll", ".bat", ".cmd"})
            self.allowed_schemes.update({"http"})  # Allow HTTP

        # Add known malicious domains (this would be populated from threat intelligence)
        self.blocked_domains.update({"malicious-site.com", "suspicious-domain.net"})

    def _apply_maximum_security_filters(self, info):
        """Apply maximum security filtering"""
        url_string = info.requestUrl().toString()

        # Block all JavaScript files in maximum security mode
        if url_string.endswith(".js"):
            logma.info(f"Blocked JavaScript file in maximum security mode: {url_string}")
            info.block(True)
            return

        # Block tracking and analytics
        tracking_patterns = ["analytics", "tracking", "ads", "facebook", "google-analytics"]
        if any(pattern in url_string.lower() for pattern in tracking_patterns):
            logma.info(f"Blocked tracking request: {url_string}")
            info.block(True)
            return

    def _apply_high_security_filters(self, info):
        """Apply high security filtering"""
        url_string = info.requestUrl().toString()

        # Block known ad and tracking domains
        ad_patterns = ["/ads/", "/ad/", "doubleclick", "googlesyndication"]
        if any(pattern in url_string.lower() for pattern in ad_patterns):
            logma.info(f"Blocked advertising request: {url_string}")
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
    # 18 is "preload", deprecated in Chromium
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

    #: The URL of the page being shown.
    first_party_url: Optional[NchantdURL]

    #: The URL of the file being requested.
    request_url: NchantdURL

    is_blocked: bool = False

    #: The resource type of the request. None if not supported on this backend.
    resource_type: Optional[ResourceType] = None

    def block(self) -> None:
        """Block this request."""
        self.is_blocked = True

    def redirect(self, url: NchantdURL, *, ignore_unsupported: bool = False) -> None:
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
        # Will be overridden if the backend supports redirection
        raise NotImplementedError


class CloudflareHandler(pyqt.QWebEngineView):
    """Handler for Cloudflare challenges"""

    challenge_detected = pyqt.Signal()
    challenge_completed = pyqt.Signal()
    challenge_failed = pyqt.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.challenge_timer = QTimer()
        self.challenge_timer.timeout.connect(self.check_challenge_status)
        self.page().loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, success):
        """Check for Cloudflare challenge after page load"""
        if success:
            self.detect_cloudflare_challenge()

    def detect_cloudflare_challenge(self):
        """Detect if a Cloudflare challenge is present"""
        js_code = """
        (function() {
            // Check for various Cloudflare challenge indicators
            const challengeSelectors = [
                '.cf-browser-verification',
                '.cf-checking-browser',
                '[data-sitekey]',
                '#challenge-form',
                '.challenge-container',
                'input[name="cf_captcha_kind"]'
            ];

            let challengeFound = false;
            let challengeType = null;

            for (const selector of challengeSelectors) {
                const element = document.querySelector(selector);
                if (element) {
                    challengeFound = true;
                    challengeType = selector;
                    break;
                }
            }

            // Check for Turnstile widget specifically
            const turnstileWidget = document.querySelector('[data-sitekey]');
            const isTurnstile = turnstileWidget !== null;

            return {
                challenge_detected: challengeFound,
                challenge_type: challengeType,
                is_turnstile: isTurnstile,
                page_title: document.title,
                url: window.location.href,
                ready_state: document.readyState
            };
        })();
        """

        self.page().runJavaScript(js_code, self.handle_challenge_detection)

    def handle_challenge_detection(self, result):
        """Handle challenge detection result"""
        if result and result.get("challenge_detected"):
            logger.info(f"Cloudflare challenge detected: {result.get('challenge_type')}")
            self.challenge_detected.emit()

            # Start monitoring for challenge completion
            self.challenge_timer.start(1000)  # Check every second

            # If it's a Turnstile widget, try to help it render
            if result.get("is_turnstile"):
                self.help_turnstile_render()
        else:
            logger.debug("No Cloudflare challenge detected")

    def help_turnstile_render(self):
        """Help Turnstile widget render properly"""
        js_code = """
        (function() {
            // Force Turnstile to re-initialize
            if (window.turnstile && window.turnstile.render) {
                const widgets = document.querySelectorAll('[data-sitekey]');
                widgets.forEach(function(widget, index) {
                    if (!widget.innerHTML.trim()) {
                        try {
                            const sitekey = widget.getAttribute('data-sitekey');
                            if (sitekey) {
                                window.turnstile.render(widget, {
                                    sitekey: sitekey,
                                    callback: function(token) {
                                        console.log('Turnstile completed:', token);
                                    }
                                });
                            }
                        } catch (e) {
                            console.log('Turnstile render error:', e);
                        }
                    }
                });
            }

            // Also try triggering resize events which can help with rendering
            window.dispatchEvent(new Event('resize'));

            return {
                turnstile_available: typeof window.turnstile !== 'undefined',
                widgets_found: document.querySelectorAll('[data-sitekey]').length
            };
        })();
        """

        self.page().runJavaScript(js_code, lambda result: logger.debug("Turnstile help result: %s", result))

    def check_challenge_status(self):
        """Periodically check if challenge is completed"""
        js_code = """
        (function() {
            // Check if we're still on a challenge page
            const challengeSelectors = [
                '.cf-browser-verification',
                '.cf-checking-browser',
                '#challenge-form'
            ];

            let stillChallenging = false;
            for (const selector of challengeSelectors) {
                if (document.querySelector(selector)) {
                    stillChallenging = true;
                    break;
                }
            }

            // Check if Turnstile is completed
            const turnstileCompleted = document.querySelector('input[name="cf-turnstile-response"]')?.value || false;

            return {
                still_challenging: stillChallenging,
                turnstile_completed: !!turnstileCompleted,
                current_url: window.location.href,
                page_title: document.title
            };
        })();
        """

        self.page().runJavaScript(js_code, self.handle_challenge_status)

    def handle_challenge_status(self, result):
        """Handle challenge status check"""
        if result:
            if not result.get("still_challenging") and result.get("turnstile_completed"):
                logger.info("Cloudflare challenge completed!")
                self.challenge_timer.stop()
                self.challenge_completed.emit()


#
#
# #: Type annotation for an interceptor function.
# InterceptorType = Callable[[NchantdRequest], None]
#
#
# _interceptors: list[InterceptorType] = []
#
#
#
# def register(interceptor: InterceptorType) -> None:
#     _interceptors.append(interceptor)
#
#
# def run(info: NchantdRequest) -> None:
#     for interceptor in _interceptors:
#         interceptor(info)
#
# class SecureRequestInterceptor(QWebEngineUrlRequestInterceptor):
#     """Security-enhanced request interceptor"""
#
#     def __init__(self, security_manager: CrossPlatformSecurityManager, parent=None):
#         super().__init__(parent)
#         self.security_manager = security_manager
#         self.security_level = security_manager.security_config["security_level"]
#
#         # Define security rules based on security level
#         self._setup_security_rules()
#
#     def _setup_security_rules(self):
#         """Setup security rules based on security level"""
#
#         self.blocked_domains = set()
#         self.blocked_extensions = set()
#         self.allowed_schemes = {"https", "data"}
#
#         if self.security_level == "maximum":
#             # Maximum security: very restrictive
#             self.blocked_extensions.update({".exe", ".dll", ".bat", ".cmd", ".scr"})
#             self.allowed_schemes = {"https"}  # Only HTTPS
#
#         elif self.security_level == "high":
#             # High security: moderately restrictive
#             self.blocked_extensions.update({".exe", ".dll", ".bat", ".cmd"})
#             self.allowed_schemes.update({"http"})  # Allow HTTP
#
#         # Add known malicious domains (this would be populated from threat intelligence)
#         self.blocked_domains.update({"malicious-site.com", "suspicious-domain.net"})
#
#     def interceptRequest(self, info):
#         """Intercept and filter requests based on security policy"""
#
#         url = info.requestUrl()
#         url_string = url.toString()
#
#         # Log request for security monitoring
#         logma.info(f"Request intercepted: {url_string}")
#
#         # Check URL scheme
#         if url.scheme() not in self.allowed_schemes:
#             logma.info(f"Blocked request with disallowed scheme: {url.scheme()}")
#             info.block(True)
#             return
#
#         # Check for blocked domains
#         host = url.host().lower()
#         if host in self.blocked_domains:
#             logma.info(f"Blocked request to suspicious domain: {host}")
#             info.block(True)
#             return
#
#         # Check for blocked file extensions
#         path = url.path().lower()
#         for ext in self.blocked_extensions:
#             if path.endswith(ext):
#                 logma.info(f"Blocked request for dangerous file: {path}")
#                 info.block(True)
#                 return
#
#         # Security level specific filtering
#         if self.security_level == "maximum":
#             self._apply_maximum_security_filters(info)
#         elif self.security_level == "high":
#             self._apply_high_security_filters(info)
#
#     def _apply_maximum_security_filters(self, info):
#         """Apply maximum security filtering"""
#         url_string = info.requestUrl().toString()
#
#         # Block all JavaScript files in maximum security mode
#         if url_string.endswith(".js"):
#             logma.info(f"Blocked JavaScript file in maximum security mode: {url_string}")
#             info.block(True)
#             return
#
#         # Block tracking and analytics
#         tracking_patterns = ["analytics", "tracking", "ads", "facebook", "google-analytics"]
#         if any(pattern in url_string.lower() for pattern in tracking_patterns):
#             logma.info(f"Blocked tracking request: {url_string}")
#             info.block(True)
#             return
#
#     def _apply_high_security_filters(self, info):
#         """Apply high security filtering"""
#         url_string = info.requestUrl().toString()
#
#         # Block known ad and tracking domains
#         ad_patterns = ["/ads/", "/ad/", "doubleclick", "googlesyndication"]
#         if any(pattern in url_string.lower() for pattern in ad_patterns):
#             logma.info(f"Blocked advertising request: {url_string}")
#             info.block(True)
#             return


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
