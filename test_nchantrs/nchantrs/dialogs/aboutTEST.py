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
    -(WT)-: -32  # 2025-11-06 22:20:49
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:20:49
import tempfile  # 2025-11-06 22:20:49
import os  # 2025-11-06 22:20:49

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:20:49
import dirname  # 2025-11-06 22:20:49
import Logma  # 2025-11-06 22:20:49
from nchantrs.dialogs.about import AboutDialog  # 2025-11-06 22:20:49

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:20:49

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:20:49
LOGMA = Logma(__name__)  # 2025-11-06 22:20:49
PXCFG = join(HERE, "_data_", "aboutTEST.yaml")  # 2025-11-06 22:20:49
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:20:49
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:20:49
TEST_000 = 1  # 2025-11-06 22:20:49

# ====================================================================================================================||


class Test_AboutDialog:  # 2025-11-06 22:20:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:20:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:20:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:20:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:20:50
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_about(self):  # 2025-11-06 22:20:50
        """"""
        if TEST_000:
            pass

    def test_requestDataCollectionPermission(self):  # 2025-11-06 22:20:50
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:20:50
        """"""
        if TEST_000:
            pass

    def test___setupUi(self):  # 2025-11-06 22:20:50
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:20:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:20:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:20:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:20:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:20:50
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:20:49


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
