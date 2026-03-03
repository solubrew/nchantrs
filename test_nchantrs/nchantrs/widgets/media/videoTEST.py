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
    -(WT)-: -32  # 2025-11-06 22:27:50
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:50
import tempfile  # 2025-11-06 22:27:50
import os  # 2025-11-06 22:27:50

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:50
import dirname  # 2025-11-06 22:27:50
import Logma  # 2025-11-06 22:27:50
from nchantrs.widgets.media.video import NchantdVideo  # 2025-11-06 22:27:50
from nchantrs.widgets.media.video import NchantdVideoPlayer  # 2025-11-06 22:27:50
from nchantrs.widgets.media.video import NchantdScreenCapture  # 2025-11-06 22:27:50
from nchantrs.widgets.media.video import NchantdDualVideoPlayer  # 2025-11-06 22:27:50

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:50

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:50
LOGMA = Logma(__name__)  # 2025-11-06 22:27:50
PXCFG = join(HERE, "_data_", "videoTEST.yaml")  # 2025-11-06 22:27:50
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:50
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:50
TEST_000 = 1  # 2025-11-06 22:27:50

# ====================================================================================================================||


class Test_NchantdVideo:  # 2025-11-06 22:27:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:50
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_play_video(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass


class Test_NchantdVideoPlayer:  # 2025-11-06 22:27:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:50
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass


class Test_NchantdScreenCapture:  # 2025-11-06 22:27:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:50
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass


class Test_NchantdDualVideoPlayer:  # 2025-11-06 22:27:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:50
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:50
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:50
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:50
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:50
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:50
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:50
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:50


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
