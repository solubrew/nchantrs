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
    -(WT)-: -32  # 2025-11-06 22:27:17
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:17
import tempfile  # 2025-11-06 22:27:17
import os  # 2025-11-06 22:27:17

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:17
import dirname  # 2025-11-06 22:27:17
import Logma  # 2025-11-06 22:27:17
from nchantrs.widgets.items.subtrees import NchantdSubTree  # 2025-11-06 22:27:17
from nchantrs.widgets.items.subtrees import NchantdProjectSubTree  # 2025-11-06 22:27:17
from nchantrs.widgets.items.subtrees import NchantdFileSystemSubTree  # 2025-11-06 22:27:17

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:17

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:17
LOGMA = Logma(__name__)  # 2025-11-06 22:27:17
PXCFG = join(HERE, "_data_", "subtreesTEST.yaml")  # 2025-11-06 22:27:17
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:17
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:17
TEST_000 = 1  # 2025-11-06 22:27:17

# ====================================================================================================================||


class Test_NchantdSubTree:  # 2025-11-06 22:27:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:17
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass


class Test_NchantdProjectSubTree:  # 2025-11-06 22:27:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:17
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass


class Test_NchantdFileSystemSubTree:  # 2025-11-06 22:27:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:17
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:17
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:17
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:17
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:17
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:17
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:17
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:17


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
