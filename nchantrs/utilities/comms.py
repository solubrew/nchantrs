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
import subprocess

# ======================================3rd Party Library Modules=====================================================||
import zmq

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.widgets.managers import NchantdManager
from pyularity.pyularity import Pyularity

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdCommunicationsManager(object):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdCommunicationsManager").override(cfg)
        self.socket = None
        self.reply = None
        self.supervisor = Pyularity()

    def initManager(self):
        """"""
        self.connect()
        return self

    def connect(self, server="tcp://127.0.0.1", port="5555"):
        """"""
        self.context = zmq.Context()  # Create a ZeroMQ context
        self.socket = self.context.socket(zmq.REQ)  # Create a REQ (Request) socket
        self.socket.connect(f"{server}:{port}")  # Connect to the server's socket
        return self

    def notice_app_failed(self, e):
        """"""
        logma.info(f"App Failed: {e}")
        message = f"APPFAILED:{self.parent.instance.instance_id}"
        return self.send_request(message)

    def start_supervisor(self):
        """"""
        self.supervisor.launch_independent()
        return self

    def request_new_instance(self):
        """"""
        message = f"NEWINSTANCE:{self.parent.instance.instance_id}"
        return self.send_request(message)

    def request_restart_instance(self, instance):
        """"""

    def send_request(self, message):
        """"""
        logma.info(f"Send Message: {message}")
        # try:
        # Send a request
        self.socket.send_string(message)

        # Set up a poller
        poller = zmq.Poller()
        poller.register(self.socket, zmq.POLLIN)

        # Wait for response with timeout (in milliseconds)
        timeout = 5000  # 5 seconds
        socks = dict(poller.poll(timeout))

        if self.socket in socks and socks[self.socket] == zmq.POLLIN:
            # Receive the response if available
            reply = self.socket.recv_string()
        else:
            # need to start communications bridge
            logma.info(f"No Response")
            self.start_supervisor()
        # except zmq.error.ZMQError as e:
        #     # Handle any other ZeroMQ-specific errors
        #     print(f"ZMQ Error: {e}")
        # finally:
        #     # Clean up
        #     self.socket.close()
        #     # self.context.term()
        # self.socket.send_string(message)
        # # TODO: need to check to see if server is running
        # #  if not then need a backup option
        # #  Wait for the reply from the server
        # self.reply = self.socket.recv_string()  # Receive UTF-8 string
        logma.info(f"Received Reply: {reply}")
        return reply


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
