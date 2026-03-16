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
    -(WT)-: -32  # 2025-11-06 22:27:28
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import json  # 2025-11-06 22:27:28
import tempfile  # 2025-11-06 22:27:28
import os  # 2025-11-06 22:27:28

# ======================================3rd Party Library Modules=====================================================||
import join  # 2025-11-06 22:27:28
import dirname  # 2025-11-06 22:27:28
import Logma  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdTreeNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdCanvasNodeMixin  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdRectangleNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdEllipseNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdCircleNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdLineNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdLineArrowNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdLineDoubleArrowNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdImageNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdTextNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdIrregularShapeNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdPolygonNode  # 2025-11-06 22:27:28
from nchantrs.widgets.items.nodes import NchantdTriangleNode  # 2025-11-06 22:27:28

# =========================================Local Library Modules======================================================||
import condor  # 2025-11-06 22:27:28

# ====================================================================================================================||
HERE = join(dirname(__file__))  # 2025-11-06 22:27:28
LOGMA = Logma(__name__)  # 2025-11-06 22:27:28
PXCFG = join(HERE, "_data_", "nodesTEST.yaml")  # 2025-11-06 22:27:28
CFG = condor.Instruct(PXCFG).load().dikt  # 2025-11-06 22:27:28
FIXTURES = condor.Instruct(join(HERE, "..", "fixtures", "fixtures.yaml")).load().dikt  # 2025-11-06 22:27:28
TEST_000 = 1  # 2025-11-06 22:27:28

# ====================================================================================================================||


class Test_NchantdNode:  # 2025-11-06 22:27:28
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:28
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:28
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:28
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:28
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_addChildNode(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_addSibilingNode(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_data(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_deleteChildren(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_hasChildren(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initContextMenu(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initModel(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initTriggers(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initUI(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_loadChildren(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onDelete(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onDeselection(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onEnter(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onExpand(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onLeftClick(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onLeftDoubleClick(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onMiddleClick(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onRightClick(self):  # 2025-11-06 22:27:28
        """"""
        if TEST_000:
            pass

    def test_onSelection(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_update_position(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__set_font(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdTreeNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_addChildNode(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_addSibilingNode(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_debounced_sort(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_deleteChildren(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_get_children(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_hasChildren(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_loadChildren(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_setText(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_set_data_focus(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_set_expanded(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_set_recent_tabs(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_sortChildren(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_sort_by_criteria(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_sort_with_lazy_loading(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_updateTabs(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__batch_update_positions(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__individual_updates_with_transaction(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__perform_sort(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__set_font(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__set_font_color(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__set_icon(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test__update_tree_ui(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdCanvasNodeMixin:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_launch_update_sigil(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdRectangleNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdEllipseNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdCircleNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdLineNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdLineArrowNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdLineDoubleArrowNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdImageNode:  # 2025-11-06 22:27:29
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:29
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:29
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:29
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:29
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:29
        """"""
        if TEST_000:
            pass


class Test_NchantdTextNode:  # 2025-11-06 22:27:30
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:30
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:30
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:30
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:30
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass


class Test_NchantdIrregularShapeNode:  # 2025-11-06 22:27:30
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:30
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:30
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:30
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:30
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass


class Test_NchantdPolygonNode:  # 2025-11-06 22:27:30
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:30
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:30
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:30
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:30
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass


class Test_NchantdTriangleNode:  # 2025-11-06 22:27:30
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:30
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:30
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:30
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:30
        """Executes a series of test functions in a sequential logic."""

        return self

    def test_initModel(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initView(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test_initWidget(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass

    def test___init__(self):  # 2025-11-06 22:27:30
        """"""
        if TEST_000:
            pass


class Test_Functions:  # 2025-11-06 22:27:30
    """"""

    @classmethod
    def setup_class(cls):  # 2025-11-06 22:27:30
        """"""

        return cls()

    @classmethod
    def teardown_class(cls):  # 2025-11-06 22:27:30
        """"""

        return

    def reset(self):  # 2025-11-06 22:27:30
        """"""
        self.setup_class()
        return self

    def test_all(self):  # 2025-11-06 22:27:30
        """Executes a series of test functions in a sequential logic."""

        return self


# ====================================================================================================================||
"""

  # 2025-11-06 22:27:28


"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
