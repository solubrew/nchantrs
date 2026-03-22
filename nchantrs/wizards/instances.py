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

import logging


logger = logging.getLogger(__name__)
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.wizards.wizards import NchantdWizard
from nchantrs.wizards.pages import NchantdSelectInstancePage
from nchantrs.models.models import NchantdInstance

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", "instances.yaml")
pxcfg = {}


class NchantdNewInstanceWizard(NchantdWizard):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdNewInstanceWizard"))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.app_pages = {}
        self.app = self.parent.app
        self.instance = self.app.model.instance
        self.is_install_active = self.parent.is_install_active
        self.select_instance = None

    def initModel(self, cfg=None):
        """"""
        super().initModel()
        return self

    def initView(self, cfg=None):
        """"""
        super().initView()
        self.select_instance = NchantdSelectInstancePage(self).initWidget()
        self.addPage(self.select_instance)
        # only if an instance is not selected
        self.create_instance()
        return self

    def initWidget(self, cfg=None):
        """"""
        self.initModel()
        self.initView()
        return self

    def initWizard(self, cfg=None):
        """"""
        self.initModel(cfg)
        self.initView(cfg)
        self.show()
        self.exec_()
        return self

    def create_database_instance(self, instance):
        """"""
        self.app.model.store.init_database_instance(instance, attach=True)
        objects = self.config.dikt["dstruct"]["database"]["attach"]
        new_objects = {"view": {}}
        for key, value in objects["view"].items():
            value["cmd"] = value["cmd"].replace("<[instance_id]>", instance.alias)
            new_objects["view"][f"{key}{instance.alias}"] = value
        # attach database to application and then create these tables
        self.app.model.store.attach_database(instance, new_objects)
        objects = self.app.model.config.dikt["dstruct"]["database"]["objects"]
        logma.info(f"Docs {self.app.model.store.docs.keys()}")
        self.app.model.store.create_objects(objects, instance.instance_id)
        # self.app.model.store.cache_app_install("installed", ["create_database"])
        return True

    def create_instance(self, instance=None):
        """"""
        logma.info(f"Wizard: create_instance: {instance}")
        instance = NchantdInstance(self, instance)
        instance.is_install_active = self.is_install_active
        logma.info(f"Install Active: {instance.is_install_active}")
        if not instance.is_install_active:
            logma.info("Set Library Instance Path")
            instance.set_instance_path(join(self.app.model.library_path, "instances", instance.instance_id))
            self.create_database_instance(instance)
        else:
            logma.info("Set Instance Path")
            instance.set_instance_path(self.app.model.application_path)
        self.app.model.add_instance(instance)
        # This needs to happen for the first instance but not on new instance creation
        self.app.model.set_instance_active(instance)
        self.app.model.store_instance(instance)
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
