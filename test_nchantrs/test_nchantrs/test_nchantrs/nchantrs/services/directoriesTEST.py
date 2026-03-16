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
    -(WT)-: -32  # 2025-11-06 22:22:25
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:22:25
import tempfile  # 2025-11-06 22:22:25
import os  # 2025-11-06 22:22:25

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:22:25
import dirname  # 2025-11-06 22:22:25
import Logma  # 2025-11-06 22:22:25
from nchantrs.services.directories import SandboxDirectories  # 2025-11-06 22:22:25
from nchantrs.services.directories import PeerDirectories  # 2025-11-06 22:22:25
from nchantrs.services.directories import SystemDirectories  # 2025-11-06 22:22:25
from nchantrs.services.directories import UserDirectories  # 2025-11-06 22:22:25

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:22:25

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:22:25
LOGMA = Logma(__name__)  # 2025-11-06 22:22:25
PXCFG = join(HERE, "_data_", "directoriesTEST.yaml")  # 2025-11-06 22:22:25
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:22:25
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:22:25
TEST_000 = 1  # 2025-11-06 22:22:25

# ====================================================================================================================||


class Test_SandboxDirectories:  # 2025-11-06 22:22:25
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:25
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:25
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:25
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:25
        """Executes a series of test functions in a sequential logic."""

        return self


class Test_PeerDirectories:  # 2025-11-06 22:22:25
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:25
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:25
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:25
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:25
        """Executes a series of test functions in a sequential logic."""

        return self


class Test_SystemDirectories:  # 2025-11-06 22:22:25
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:25
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:25
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:25
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:25
        """Executes a series of test functions in a sequential logic."""

        return self


class Test_UserDirectories:  # 2025-11-06 22:22:25
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:25
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:25
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:25
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:25
        """Executes a series of test functions in a sequential logic."""

        return self


class Test_Functions:  # 2025-11-06 22:22:25
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:22:25
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:22:25
        """"""

        return

    def reset(self):  # 2025-11-06 22:22:25
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:22:25
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:22:25


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
