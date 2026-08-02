from typing import Any
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
import logging
from nchantrs.services.telemetry import TelemetryService
logger = logging.getLogger(__name__)
from kahndor.logma import Logma
from sentinel.sentinel import Sentinel, Automaton
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'agents.yaml')

class NchantdSentinelManager(object):
    """What should I do?"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.config = kahndor.Instruct(pxcfg).select('NchantdSentinelManager').override(cfg)
        self.agents = []

    def initAgents(self) -> Any:
        """"""
        self.agent.initWidget()
        if self.model.are_mini_games_active:
            self.agent.initMiniGamesAgent()
        if self.model.is_internal_server_active:
            self.agent.initServerAgent()
        if self.model.are_services_active:
            self.agent.initServicesAgent()
        self.model.store.store_app_event('initialized', 'application agents initialized')
        return self

    def assign_agent(self, focus) -> Any:
        """"""
        agent = NchantdAgent().set_focus(focus)
        self.agents.append(agent)
        return agent

class NchantdSentinel(Sentinel):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg)
        if parent is not None:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent.application_name, self.config)
        self.tasks = {}

    def initModel(self) -> Any:
        """
        setup recuring system tasks that need to be ran like sending telemetry data to the server

        :return:
        """
        self.tasks['telemetry'] = {}
        self.tasks['telemetry']['object'] = TelemetryService()
        self.tasks['telemetry']['function'] = 'send_data'
        self.tasks['telemetry']['args'] = []
        self.tasks['telemetry']['cycle'] = '24HRS'
        self.tasks['cleanup_database'] = {}
        self.tasks['cleanup_database']['object'] = self.parent.model
        self.tasks['cleanup_database']['function'] = 'cleanup_database'
        self.tasks['cleanup_database']['args'] = []
        self.tasks['cleanup_database']['cycle'] = '24HRS'
        return self

    def initView(self) -> Any:
        super().initView()
        logma.info(f'initView {{type(self).__name__}}')
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdAgent(Automaton):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def init(self) -> None:
        """"""
        self.on()

    def set_focus(self, object) -> Any:
        """"""
        super().set_focus(object)
        return self