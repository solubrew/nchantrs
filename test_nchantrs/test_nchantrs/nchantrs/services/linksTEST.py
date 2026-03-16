# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
-(META)-:
    docid: <[uuid]>
    name: <[file name]>
    description: >
      <[description]>
    expiry: <[expiration]>
    version: <[version]>
    authority: <[authority]>
    security: <[security]>
    -(WT)-: -32  # 2025-11-06 22:22:17
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:22:17
import tempfile  # 2025-11-06 22:22:17
import os  # 2025-11-06 22:22:17

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:22:17
import dirname  # 2025-11-06 22:22:17
import Logma  # 2025-11-06 22:22:17
from nchantrs.services.links import LinkService  # 2025-11-06 22:22:17

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:22:17

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:22:17
LOGMA = Logma(__name__)  # 2025-11-06 22:22:17
PXCFG = join(HERE, "_data_", "linksTEST.yaml")  # 2025-11-06 22:22:17
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:22:17
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:22:17
TEST_000 = 1  # 2025-11-06 22:22:17

# ====================================================================================================================||


class Test_LinkService:  # 2025-11-06 22:22:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:17
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_get_links(self):  # 2025-11-06 22:22:17
        """"""
        if TEST_000:
            pass

    def test_store_link(self):  # 2025-11-06 22:22:17
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:22:17
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:22:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:17
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:22:17


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
