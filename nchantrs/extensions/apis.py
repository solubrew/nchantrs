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
import json as j

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "apis.yaml")


class NchantdEventAPI(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdEventAPI").override(cfg)
        self.eventTriggered = pyqt.Signal(str)

    def triggerEvent(self, event_name):
        """
        Trigger an event from Python to JavaScript.
        """
        self.eventTriggered.emit(event_name)


class NchantdNetworkAPI(pyqt.QObject):
    """"""

    def __init__(self, profile):
        """"""
        super().__init__()
        self.profile = profile
        self.profile.setRequestInterceptor(self)
        self.requestIntercepted = pyqt.Signal(str, str, str)  # Signal for request interception (method, URL, headers)

    def interceptRequest(self, info: pyqt.QWebEngineUrlRequestInfo):
        """
        Handle intercepted requests from QWebEngineProfile.
        """
        # Extract request details
        method = info.requestMethod().data().decode()  # GET/POST
        url = info.requestUrl().toString()
        headers = info.requestHeaders()

        # Emit request details to JavaScript or extensions
        self.requestIntercepted.emit(method, url, str(headers))

        # Example modification: Block specific URLs
        if "example.com" in url:
            info.block(True)  # Block the request
        else:
            info.block(False)  # Let the request through

    @pyqt.Slot(result=str)
    def enableBlocking(self):
        """
        Enable JavaScript-triggered blocking of certain websites.
        """
        self.blocking = True
        return "Blocking Enabled"

    @pyqt.Slot(result=str)
    def disableBlocking(self):
        """
        Disable JavaScript-triggered blocking.
        """
        self.blocking = False
        return "Blocking Disabled"


class NchantdNodesAPI(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)

    @pyqt.Slot(str)
    def create(self, url):
        """
        Open a new tab (or window in WebView terms) with the given URL.
        """
        new_tab = pyqt.QWebEngineView()
        new_tab.setUrl(url)
        new_tab.show()

    @pyqt.Slot(str)
    def executeScript(self, script):
        """
        Execute JavaScript in the active tab.
        """
        current_page = self.parentView.page()  # Access parent page dynamically
        current_page.runJavaScript(script)


class NchantdRuntimeAPI(object):
    """"""

    messageReceived = pyqt.Signal(str)  # Signal for receiving messages

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)

    @pyqt.Slot(str)
    def sendMessage(self, message):
        """
        Send a message from Python to JavaScript.
        """
        self.messageReceived.emit(message)

    @pyqt.Slot(str, result=str)
    def handleIncomingMessage(self, message):
        """
        Handle a message sent from JavaScript.
        """
        print(f"Received message from JavaScript: {message}")
        response = {"response": f"Python received: {message}"}
        return json.dumps(response)


class NchantdSourceAPI(object):
    """Make connected data sources available to other extensions will need security"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdSourceAPI").override(cfg)

    def load_source(self):
        """"""

    def update_source(self):
        """"""

    def save_source(self):
        """"""


class NchantdStorageAPI(object):
    """"""

    def __init__(self, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdStorageAPI").override(cfg)
        self.storage_file = "storage.json"  # connect to database storage
        self.load_storage()

    def load_storage(self):
        try:
            with open(self.storage_file, "r") as f:
                self.data = j.load(f)
        except FileNotFoundError:
            self.data = {}

    def save_storage(self):
        with open(self.storage_file, "w") as f:
            j.dump(self.data, f)

    @pyqt.Slot(str, str)
    def set(self, key, value):
        self.data[key] = value
        self.save_storage()

    @pyqt.Slot(str, result=str)
    def get(self, key):
        return self.data.get(key, None)


class NchantdWebRequestAPI(object):
    """"""

    def __init__(self, profile, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("").override(cfg)
        self.profile = profile
        self.intercept_requests()

    def intercept_requests(self):
        self.profile.requestIntercepted.connect(self.handle_request)

    def handle_request(self, intercepted_request):
        if "google.com" in intercepted_request.url().toString():
            intercepted_request.abort()  # Block the request
        else:
            intercepted_request.continueRequest()


# Handle Python-JavaScript communication using QWebChannel
class NchantdExtensionAPI(pyqt.QObject):
    def __init__(self, parent=None, cfg=None):
        self.config = condor.Instruct(pxcfg).select("NchantdExtensionAPI").override(cfg)
        super().__init__(parent)
        profile = None
        if profile:
            self.network = NchantdNetworkAPI(profile)
            self.webRequest = NchantdWebRequestAPI(profile)
        self.runtime = NchantdRuntimeAPI()
        self.source = NchantdSourceAPI()
        self.storage = NchantdStorageAPI()
        self.nodes = NchantdNodesAPI()

    @pyqt.Slot(str, result=str)
    def handleRequest(self, request):
        """
        Handle extension API requests from JavaScript.

        Args:
            request (str): The JSON string containing the incoming request.

        Returns:
            str: A JSON string as the response to the JavaScript call.
        """
        request_data = j.loads(request)
        method = request_data.get("method")
        params = request_data.get("params", {})

        # Example methods for the extension
        if method == "getAccounts":
            response = {"accounts": ["0xYourEthereumAddress"]}
        elif method == "signMessage":
            response = {"signature": "0xFakeSignature"}
        else:
            response = {"error": "Unknown method"}

        # Return the response as a JSON string
        return j.dumps(response)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
