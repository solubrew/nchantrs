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
    -(WT)-: -32  # 2025-11-06 22:22:40
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:22:40
import tempfile  # 2025-11-06 22:22:40
import os  # 2025-11-06 22:22:40

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:22:40
import dirname  # 2025-11-06 22:22:40
import Logma  # 2025-11-06 22:22:40
from nchantrs.themes.images import BackgroundImages  # 2025-11-06 22:22:40

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:22:40

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:22:40
LOGMA = Logma(__name__)  # 2025-11-06 22:22:40
PXCFG = join(HERE, "_data_", "imagesTEST.yaml")  # 2025-11-06 22:22:40
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:22:40
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:22:40
TEST_000 = 1  # 2025-11-06 22:22:40

# ====================================================================================================================||


class Test_BackgroundImages:  # 2025-11-06 22:22:40
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:40
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:40
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:40
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:40
        """Executes a series of test functions in a sequential logic."""

        return self

    def test___init__(self):  # 2025-11-06 22:22:40
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:22:40
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:40
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:40
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:40
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:40
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:22:40


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
