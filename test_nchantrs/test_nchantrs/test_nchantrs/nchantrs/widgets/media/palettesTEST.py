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
    -(WT)-: -32  # 2025-11-06 22:27:52
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:52
import tempfile  # 2025-11-06 22:27:52
import os  # 2025-11-06 22:27:52

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:52
import dirname  # 2025-11-06 22:27:52
import Logma  # 2025-11-06 22:27:52
from nchantrs.widgets.media.palettes import NchantdPaletteTable  # 2025-11-06 22:27:52
from nchantrs.widgets.media.palettes import NchantdPalette  # 2025-11-06 22:27:52

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:52

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:52
LOGMA = Logma(__name__)  # 2025-11-06 22:27:52
PXCFG = join(HERE, "_data_", "palettesTEST.yaml")  # 2025-11-06 22:27:52
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:52
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:52
TEST_000 = 1  # 2025-11-06 22:27:52

# ====================================================================================================================||


class Test_NchantdPaletteTable:  # 2025-11-06 22:27:52
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:52
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:52
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:52
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:52
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass


class Test_NchantdPalette:  # 2025-11-06 22:27:52
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:52
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:52
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:52
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:52
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:52
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:52
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:52
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:52
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:52
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:52
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:52


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
