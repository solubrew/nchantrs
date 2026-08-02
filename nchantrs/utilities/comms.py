from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
import datetime as dt
import subprocess
import zmq
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.managers import NchantdManager
here = join(dirname(__file__), '')
log = True
logma = Logma(__name__)
pxcfg = join(here, '_data_', '.yaml')

class NchantdCommunicationsManager(object):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdCommunicationsManager').override(cfg)
        self.socket = None
        self.reply = None

    def initManager(self) -> Any:
        """"""
        self.connect()
        return self

    def connect(self, server='tcp://127.0.0.1', port='5555') -> Any:
        """"""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f'{server}:{port}')
        return self

    def notice_app_failed(self, e) -> Any:
        """"""
        logma.info(f'App Failed: {e}')
        message = f'APPFAILED:{self.parent.instance.instance_id}'
        return self.send_request(message)

    def start_supervisor(self) -> Any:
        """"""
        self.supervisor.launch_independent()
        return self

    def request_new_instance(self) -> Any:
        """"""
        message = f'NEWINSTANCE:{self.parent.instance.instance_id}'
        return self.send_request(message)

    def request_restart_instance(self, instance) -> None:
        logma.info(f'request_restart_instance called')
        return self

    def send_request(self, message) -> Any:
        """"""
        logma.info(f'Send Message: {message}')
        self.socket.send_string(message)
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)
        timeout = 5000
        socks = dict(poller.poll(timeout))
        if self.socket in socks and socks[self.socket] == zmq.POLLIN:
            reply = self.socket.recv_string()
        else:
            logma.info(f'No Response')
            self.start_supervisor()
        logma.info(f'Received Reply: {reply}')
        return reply