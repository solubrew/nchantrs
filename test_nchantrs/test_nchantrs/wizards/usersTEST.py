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
    -(WT)-: -32  # 2025-11-06 22:28:57
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:28:57
import tempfile  # 2025-11-06 22:28:57
import os  # 2025-11-06 22:28:57

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:28:57
import dirname  # 2025-11-06 22:28:57
import Logma  # 2025-11-06 22:28:57
from nchantrs.wizards.users import NchantdNewUserWizard  # 2025-11-06 22:28:57
from nchantrs.wizards.users import NchantdTOSSignOffPage  # 2025-11-06 22:28:57
from nchantrs.wizards.users import NchantdNewUserDetailsPage  # 2025-11-06 22:28:57
from nchantrs.wizards.users import NchantdNewUserSignupPage  # 2025-11-06 22:28:57
from nchantrs.wizards.users import NchantdUserNameSelectorPage  # 2025-11-06 22:28:57

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:28:57

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:28:57
LOGMA = Logma(__name__)  # 2025-11-06 22:28:57
PXCFG = join(HERE, "_data_", "usersTEST.yaml")  # 2025-11-06 22:28:57
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:28:57
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:28:57
TEST_000 = 1  # 2025-11-06 22:28:57

# ====================================================================================================================||


class Test_NchantdNewUserWizard:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass


class Test_NchantdTOSSignOffPage:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_validatePage(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass


class Test_NchantdNewUserDetailsPage:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass


class Test_NchantdNewUserSignupPage:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass


class Test_NchantdUserNameSelectorPage:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:28:57
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:28:57
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:28:57
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:28:57
        """"""

        return

    def reset(self):  # 2025-11-06 22:28:57
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:28:57
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:28:57


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
