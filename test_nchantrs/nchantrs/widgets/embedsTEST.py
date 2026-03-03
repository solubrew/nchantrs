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
    -(WT)-: -32  # 2025-11-06 22:23:43
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:23:43
import tempfile  # 2025-11-06 22:23:43
import os  # 2025-11-06 22:23:43

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:23:43
import dirname  # 2025-11-06 22:23:43
import Logma  # 2025-11-06 22:23:43
from nchantrs.widgets.embeds import NchantdDiaEmbed  # 2025-11-06 22:23:43
from nchantrs.widgets.embeds import NchantdLibreCADEmbed  # 2025-11-06 22:23:43
from nchantrs.widgets.embeds import NchantdOpenSCADEmbed  # 2025-11-06 22:23:43
from nchantrs.widgets.embeds import NchantdTerminalEmbed  # 2025-11-06 22:23:43

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:23:43

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:23:43
LOGMA = Logma(__name__)  # 2025-11-06 22:23:43
PXCFG = join(HERE, "_data_", "embedsTEST.yaml")  # 2025-11-06 22:23:43
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:23:43
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:23:43
TEST_000 = 1  # 2025-11-06 22:23:43

# ====================================================================================================================||


class Test_NchantdDiaEmbed:  # 2025-11-06 22:23:43
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:23:43
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:23:43
        """"""

        return

    def reset(self):  # 2025-11-06 22:23:43
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:23:43
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass


class Test_NchantdLibreCADEmbed:  # 2025-11-06 22:23:43
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:23:43
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:23:43
        """"""

        return

    def reset(self):  # 2025-11-06 22:23:43
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:23:43
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass


class Test_NchantdOpenSCADEmbed:  # 2025-11-06 22:23:43
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:23:43
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:23:43
        """"""

        return

    def reset(self):  # 2025-11-06 22:23:43
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:23:43
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass


class Test_NchantdTerminalEmbed:  # 2025-11-06 22:23:43
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:23:43
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:23:43
        """"""

        return

    def reset(self):  # 2025-11-06 22:23:43
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:23:43
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:23:43
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:23:43
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:23:43
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:23:43
        """"""

        return

    def reset(self):  # 2025-11-06 22:23:43
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:23:43
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:23:43


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
