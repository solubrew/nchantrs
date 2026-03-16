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
    -(WT)-: -32  # 2025-11-06 22:27:07
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:07
import tempfile  # 2025-11-06 22:27:07
import os  # 2025-11-06 22:27:07

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:07
import dirname  # 2025-11-06 22:27:07
import Logma  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdCalendlyConnectTab  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdConnectTab  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdFacebookConnectTab  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdGoogleConnectTab  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdOutlookConnectTab  # 2025-11-06 22:27:07
from nchantrs.widgets.controls.connectors import NchantdXConnectTab  # 2025-11-06 22:27:07

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:07

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:07
LOGMA = Logma(__name__)  # 2025-11-06 22:27:07
PXCFG = join(HERE, "_data_", "connectorsTEST.yaml")  # 2025-11-06 22:27:07
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:07
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:07
TEST_000 = 1  # 2025-11-06 22:27:07

# ====================================================================================================================||


class Test_NchantdCalendlyConnectTab:  # 2025-11-06 22:27:07
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:07
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:07
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:07
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:07
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass


class Test_NchantdConnectTab:  # 2025-11-06 22:27:07
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:07
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:07
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:07
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:07
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass


class Test_NchantdFacebookConnectTab:  # 2025-11-06 22:27:07
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:07
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:07
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:07
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:07
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass


class Test_NchantdGoogleConnectTab:  # 2025-11-06 22:27:07
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:07
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:07
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:07
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:07
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass


class Test_NchantdOutlookConnectTab:  # 2025-11-06 22:27:07
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:07
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:07
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:07
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:07
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:07
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass


class Test_NchantdXConnectTab:  # 2025-11-06 22:27:08
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:08
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:08
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:08
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:08
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:08
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:08
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:08
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:08
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:08
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:08
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:07


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
