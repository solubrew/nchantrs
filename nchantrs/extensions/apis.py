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
from typing import Optional, Dict, List, Any, Tuple
import datetime as dt
import json as j
import logging
logger = logging.getLogger(__name__)
from kahndor import kahndor
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', 'apis.yaml')

class NchantdEventAPI(object):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdEventAPI').override(cfg)
        self.eventTriggered = pyqt.Signal(str)

    def triggerEvent(self, event_name) -> None:
        """
        Trigger an event from Python to JavaScript.
        """
        self.eventTriggered.emit(event_name)

class NchantdNetworkAPI(pyqt.QObject):
    """"""

    def __init__(self, profile) -> None:
        """"""
        super().__init__()
        self.profile = profile
        self.profile.setRequestInterceptor(self)
        self.requestIntercepted = pyqt.Signal(str, str, str)

    def interceptRequest(self, info: pyqt.QWebEngineUrlRequestInfo) -> None:
        """
        Handle intercepted requests from QWebEngineProfile.
        """
        method = info.requestMethod().data().decode()
        url = info.requestUrl().toString()
        headers = info.requestHeaders()
        self.requestIntercepted.emit(method, url, str(headers))
        if 'example.com' in url:
            info.block(True)
        else:
            info.block(False)

    @pyqt.Slot(result=str)
    def enableBlocking(self) -> None:
        """
        Enable JavaScript-triggered blocking of certain websites.
        """
        self.blocking = True
        return 'Blocking Enabled'

    @pyqt.Slot(result=str)
    def disableBlocking(self) -> None:
        """
        Disable JavaScript-triggered blocking.
        """
        self.blocking = False
        return 'Blocking Disabled'

class NchantdNodesAPI(object):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('').override(cfg)

    @pyqt.Slot(str)
    def create(self, url) -> None:
        """
        Open a new tab (or window in WebView terms) with the given URL.
        """
        new_tab = pyqt.QWebEngineView()
        new_tab.setUrl(url)
        new_tab.show()

    @pyqt.Slot(str)
    def executeScript(self, script) -> None:
        """
        Execute JavaScript in the active tab.
        """
        current_page = self.parentView.page()
        current_page.runJavaScript(script)

class NchantdRuntimeAPI(object):
    """"""
    messageReceived = pyqt.Signal(str)

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('').override(cfg)

    @pyqt.Slot(str)
    def sendMessage(self, message) -> None:
        """
        Send a message from Python to JavaScript.
        """
        self.messageReceived.emit(message)

    @pyqt.Slot(str, result=str)
    def handleIncomingMessage(self, message) -> None:
        """
        Handle a message sent from JavaScript.
        """
        logma.debug(f'Received message from JavaScript: {message}')
        response = {'response': f'Python received: {message}'}
        return json.dumps(response)

class NchantdSourceAPI(object):
    """Make connected data sources available to other extensions will need security"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdSourceAPI').override(cfg)

    def load_source(self) -> None:
        logma.info(f'load_source called')
        return self

    def update_source(self) -> None:
        logma.info(f'update_source called')
        return self

    def save_source(self) -> None:
        logma.info(f'save_source called')
        return self

class NchantdStorageAPI(object):
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdStorageAPI').override(cfg)
        self.storage_file = 'storage.json'
        self.load_storage()
        logma.info(f'NchantdStorageAPI initialized')

    def load_storage(self) -> None:
        try:
            with open(self.storage_file, 'r') as f:
                self.data = j.load(f)
        except FileNotFoundError:
            self.data = {}

    def save_storage(self) -> None:
        with open(self.storage_file, 'w') as f:
            j.dump(self.data, f)

    @pyqt.Slot(str, str)
    def set(self, key, value) -> None:
        self.data[key] = value
        self.save_storage()

    @pyqt.Slot(str, result=str)
    def get(self, key) -> None:
        return self.data.get(key, None)

class NchantdWebRequestAPI(object):
    """"""

    def __init__(self, profile, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('').override(cfg)
        self.profile = profile
        self.intercept_requests()

    def intercept_requests(self) -> None:
        self.profile.requestIntercepted.connect(self.handle_request)

    def handle_request(self, intercepted_request) -> None:
        if 'google.com' in intercepted_request.url().toString():
            intercepted_request.abort()
        else:
            intercepted_request.continueRequest()

class NchantdExtensionAPI(pyqt.QObject):

    def __init__(self, parent=None, cfg=None) -> None:
        self.config = kahndor.Instruct(pxcfg).select('NchantdExtensionAPI').override(cfg)
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
    def handleRequest(self, request) -> None:
        """
        Handle extension API requests from JavaScript.

        Args:
            request (str): The JSON string containing the incoming request.

        Returns:
            str: A JSON string as the response to the JavaScript call.
        """
        request_data = j.loads(request)
        method = request_data.get('method')
        params = request_data.get('params', {})
        if method == 'getAccounts':
            response = {'accounts': ['0xYourEthereumAddress']}
        elif method == 'signMessage':
            response = {'signature': '0xFakeSignature'}
        else:
            response = {'error': 'Unknown method'}
        return j.dumps(response)