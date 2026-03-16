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
    -(WT)-: -32  # 2025-11-06 22:25:54
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:25:54
import tempfile  # 2025-11-06 22:25:54
import os  # 2025-11-06 22:25:54

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:25:54
import dirname  # 2025-11-06 22:25:54
import Logma  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdCalendar  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdDateTimeSelect  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdDateTimeGroup  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdDateSelect  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdDateIterate  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdEventsList  # 2025-11-06 22:25:54
from nchantrs.widgets.calendars.calendars import NchantdTimeSelect  # 2025-11-06 22:25:54

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:25:54

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:25:54
LOGMA = Logma(__name__)  # 2025-11-06 22:25:54
PXCFG = join(HERE, "_data_", "calendarsTEST.yaml")  # 2025-11-06 22:25:54
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:25:54
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:25:54
TEST_000 = 1  # 2025-11-06 22:25:54

# ====================================================================================================================||


class Test_NchantdCalendar:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdDateTimeSelect:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdDateTimeGroup:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initView(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdDateSelect:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initView(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_on_date_selected(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdDateIterate:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdEventsList:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_NchantdTimeSelect:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initWidget(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:25:54
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:25:54
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:25:54
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:25:54
        """"""

        return

    def reset(self):  # 2025-11-06 22:25:54
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:25:54
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:25:54


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
