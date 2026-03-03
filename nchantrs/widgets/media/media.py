# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||
import feedparser

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox, NchantdCheckboxGroup
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.groups import NchantdVScrollGroupBox
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.managers import NchantdManager
from nchantrs.widgets.widgets import NchantdWidget
from nchantrs.widgets.panes.files import NchantdFileDetailsPane
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "media.yaml")
pxcfg = {}


class NchantdNEWSLSummary(NchantdManager):
    """Nchantd Notable Events Weather Sports and"""

    def __init__(self, parent=None, cfg={}):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdNEWSLSummaryTab")
        if parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.articles = []
        self.newsl = None

    def initModel(self):
        """"""
        super().initModel()
        # TODO move this data collection aspect to a side process and then pull from the cache for the display
        # Integrate Video uploads from Rumble, and Youtube
        # moving feeds to worldbridge
        self.newsl = self.app.model.get_rss_entries()
        logma.info(f"newsl {self.newsl}")
        return self

    def initView(self):
        """ """
        super().initView()
        cfg = {"size": ["auto", "auto"]}
        scroll = NchantdVScrollGroupBox(self, cfg)
        scroll.setTitle("Recent NEWSL")
        if self.newsl is not None:
            for feed in self.newsl.head(10).to_dict(orient="records"):
                article = NchantdNEWSLArticle(self, feed).initWidget()
                scroll.addWidget(article)
                self.articles.append(article)
        self.layout.addLayout(scroll.layout)
        return self

    def initWidget(self, pos=0):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdNEWSLArticle(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.link = None
        self.summary = None
        self.title = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        logma.info("break down the article")
        outer_layout = pyqt.QHBoxLayout()
        layout = pyqt.QVBoxLayout()

        cfg = {"text": f"{self.config.dikt.get('title_txt', None)}..."}
        if cfg.get("text", None) is not None and cfg.get("text", None) != "None" and cfg.get("text", "") != "":
            self.title = NchantdLabel(self, cfg).initWidget()
            self.title.set_size(min_width=250)
            layout.addWidget(self.title)
        else:
            return self
        cfg = {"text": f"{self.config.dikt.get('summary_txt', None)}"}
        if cfg.get("text", None) is not None and cfg.get("text", None) != "None" and cfg.get("text", "") != "":
            self.summary = NchantdLabel(self, cfg).initWidget()
            self.summary.set_size(min_width=250)
            layout.addWidget(self.summary)
        cfg = {"text": f"{self.config.dikt.get('author_txt', None)}"}
        if cfg.get("text", None) is not None and cfg.get("text", None) != "None" and cfg.get("text", "") != "":
            self.author = NchantdLabel(self, cfg).initWidget()
            self.author.set_size(min_width=250)
            layout.addWidget(self.author)
        group = pyqt.QGroupBox()
        group.setTitle(self.config.dikt.get("published_dttm", dt.datetime.now().strftime("%Y-%m-%d %H:%M")))
        group.setLayout(outer_layout)
        group.setAlignment(pyqt.Qt.AlignmentFlag.AlignTop)
        buttons = {
            0: "mark_interested",
            # have the research icon turn green when the research is ready for that article and clicking it again will jump to that nodeset
            1: "mark_research_needed",
            2: "mark_ai_summarization",
        }  # TODO build in the ability to make the button checkable
        outer_layout.addLayout(layout)
        cfg = {"layout": "vertical"}
        self.parameters = NchantdButtonBar(self, cfg).initWidget(buttons)
        outer_layout.addWidget(self.parameters)
        self.layout.addWidget(group)
        # outer_layout.addWidget(group)
        # outer_layout.addLayout(buttons_layout)
        # self.layout.addLayout(outer_layout)
        # self.layout.addSpacing(5)
        return self

    # logma.info(f"Entry {entry}")
    # logma.info(f"Entry {entry.get("title", "")}")
    # logma.info(entry.keys())
    #
    # label_layout = pyqt.QVBoxLayout()
    # title = NchantdLabel(self, cfg).initWidget()
    # label_layout.addWidget(title)
    #
    # link = NchantdLabel(self, cfg).initWidget()
    # label_layout.addWidget(link)
    # label_layout.addSpacing(20)
    # layout.layout.addLayout(label_layout)

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdFileIcon(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("Nchantd")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self


class NchantdFileViewer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None):
        """ """
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdFileViewer")
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.details_pane = None
        self.files = []
        self.viewer_item = None

    def initModel(self):
        """"""
        super().initModel()
        return self

    def initView(self):
        """"""
        super().initView()

        scroll_area = pyqt.QScrollArea(self)
        self.thumbnail_widget = self.viewer_item(total_thumbnails=100)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.thumbnail_widget)
        scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        for i in range(self.config.dikt["total_thumbnails"]):
            cfg = {"index": i + 1}
            label = self.viewer_item(self, cfg).initWidget()
            self.files.append(label)
            self.layout.addWidget(label)

        self.details_pane = NchantdFileDetailsPane(self, cfg).initWidget()
        self.layout.addWidget(self.details_pane)

        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

    def find_duplicate(self):
        """
        find duplicate files by name, size, and hash with options to use any or all of them
        :return:
        """
        return

    def lazy_load_visible_items(self, scroll_position):
        """"""
        visible_region = pyqt.QSize(self.width(), self.parent().viewport().height())  # Visible region size
        viewport_top = scroll_position
        viewport_bottom = viewport_top + visible_region.height()
        for thumb in self.files:
            thumb_top = thumb.y()
            thumb_bottom = thumb_top + thumb.height()
            if thumb_bottom > viewport_top and thumb_top < viewport_bottom:
                if thumb.pixmap() is None:
                    thumb.lazy_load_image()

    def on_scroll(self):
        scroll_position = self.centralWidget().verticalScrollBar().value()
        self.thumbnail_widget.lazy_load_visible_items(scroll_position)

    def set_viewer_item(self):
        """"""
        self.viewer_item = NchantdFileIcon
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
