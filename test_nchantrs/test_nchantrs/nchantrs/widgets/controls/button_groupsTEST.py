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
    -(WT)-: -32  # 2025-11-06 22:27:00
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:00
import tempfile  # 2025-11-06 22:27:00
import os  # 2025-11-06 22:27:00

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:00
import dirname  # 2025-11-06 22:27:00
import Logma  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdButtonGrid  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdAcceptButtons  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdOkButtons  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdSaveButtons  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdSubmissionButtons  # 2025-11-06 22:27:00
from nchantrs.widgets.controls.button_groups import NchantdTabSideButtons  # 2025-11-06 22:27:01
from nchantrs.widgets.controls.button_groups import NchantdMathPad  # 2025-11-06 22:27:01
from nchantrs.widgets.controls.button_groups import NchantdNumberPad  # 2025-11-06 22:27:01
from nchantrs.widgets.controls.button_groups import NchantdFontConfigBar  # 2025-11-06 22:27:01
from nchantrs.widgets.controls.button_groups import NchantdBorderConfigBar  # 2025-11-06 22:27:01

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:00

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:01
LOGMA = Logma(__name__)  # 2025-11-06 22:27:01
PXCFG = join(HERE, "_data_", "button_groupsTEST.yaml")  # 2025-11-06 22:27:01
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:01
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:01
TEST_000 = 1  # 2025-11-06 22:27:01

# ====================================================================================================================||


class Test_NchantdButtonGrid:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdAcceptButtons:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdOkButtons:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdSaveButtons:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdSubmissionButtons:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initWidget(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdTabSideButtons:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdMathPad:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdNumberPad:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass


class Test_NchantdFontConfigBar:  # 2025-11-06 22:27:01
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:01
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:01
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:01
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:01
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_cmd_on_change_background_color(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_bold(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_color(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_highlight_color(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_italic(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_size(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_strike(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_style(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_subscript(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_superscript(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_underline(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_underline_double(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_color_selected(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_size_selected(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_style(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_style_options(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_style_selected(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_font_styles(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_text_background_color_options(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_get_text_background_color_selected(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initModel(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:01
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_set_font_color(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_set_font_color_background(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_set_font_color_color(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_set_vertical_alignment(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass


class Test_NchantdBorderConfigBar:  # 2025-11-06 22:27:02
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:02
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:02
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:02
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:02
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_cmd_on_change_border_color(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_cmd_on_change_border_style(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_cmd_on_size_change(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_get_border_style(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_get_border_styles(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_initModel(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:02
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:02
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:02
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:02
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:02
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:02
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:00


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
