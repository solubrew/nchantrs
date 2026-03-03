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

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.services.telemetry import TelemetryService
from ogma.logma import Logma
from sentinel.sentinel import Sentinel, Automaton

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "agents.yaml")


class NchantdSentinelManager(object):
    """What should I do?"""

    def __init__(self, parent, cfg=None):
        """"""
        self.config = condor.Instruct(pxcfg).select("NchantdSentinelManager").override(cfg)
        self.agents = []

    def initAgents(self):
        """"""  # start agents to handle background functions
        self.agent.initWidget()
        if self.model.are_mini_games_active:
            self.agent.initMiniGamesAgent()  #  each agent will be an automaton
        if self.model.is_internal_server_active:
            self.agent.initServerAgent()  #  each agent will be an automaton
        if self.model.are_services_active:
            self.agent.initServicesAgent()  #  each agent will be an automaton
        self.model.store.store_app_event("initialized", "application agents initialized")
        return self

    def assign_agent(self, focus):
        """"""
        agent = NchantdAgent().set_focus(focus)
        self.agents.append(agent)
        return agent


class NchantdSentinel(Sentinel):
    """"""

    def __init__(self, parent, cfg=None):
        """"""
        self.parent = parent
        self.config = condor.Instruct(pxcfg)
        if parent is not None:
            self.config.override(parent.config)
        self.config.override(cfg)
        super().__init__(self.parent.application_name, self.config)
        self.tasks = {}

    def initModel(self):
        """
        setup recuring system tasks that need to be ran like sending telemetry data to the server

        :return:
        """
        self.tasks["telemetry"] = {}
        self.tasks["telemetry"]["object"] = TelemetryService()
        self.tasks["telemetry"]["function"] = "send_data"
        self.tasks["telemetry"]["args"] = []
        self.tasks["telemetry"]["cycle"] = "24HRS"

        self.tasks["cleanup_database"] = {}
        self.tasks["cleanup_database"]["object"] = self.parent.model
        self.tasks["cleanup_database"]["function"] = "cleanup_database"
        self.tasks["cleanup_database"]["args"] = []
        self.tasks["cleanup_database"]["cycle"] = "24HRS"

        return self

    def initView(self):
        """
        TODO: 20240723 create a dialog to monitor the status of the Sentinel
        :return:
        """
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdAgent(Automaton):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def init(self):
        """"""
        self.on()

    def set_focus(self, object):
        """"""
        super().set_focus(object)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
