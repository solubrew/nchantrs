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
from os.path import abspath, dirname, join, exists

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from squirl.objnql import txtonql
from nchantrs.libraries import pyqt

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
pxcfg = join(here, "_data_", "themes.yaml")


class NchantdTheme:
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select("NchantdTheme")
        self.themes = kahndor.Instruct(pxcfg).select("Themes").dikt
        self.config.override(self.themes).override(cfg)
        self.accent_iconset = "mist_icons"
        self.accent = None
        self.app = self.parent
        self.background = None
        self.base_iconset = "midnight_icons"
        self.color = None
        self.colors = None
        self.foreground = None
        self.highlight = None
        self.palette = None
        self.system = None
        self.theme = "midnight_frost"
        self.small_font = None
        self.medium_font = None
        self.large_font = None
        self.xlarge_font = None
        self.iconset = None
        self.focus = None

    def create_theme(self, palette, name, blob) -> None:
        """"""
        blob = blob.replace("<[primary_foreground]>", palette["primary"]["foreground"])
        blob = blob.replace("<[primary_background]>", palette["primary"]["background"])
        blob = blob.replace("<[primary_accent]>", palette["primary"]["background"])
        if name is not None:
            path = join(here, "_data_", "themes")
            txtonql.Doc(join(path, f"{name}.qss")).write(blob)
        return blob

    def import_theme(self, named_style="midnight_frost", palette=None, name=None) -> None:
        """ """
        logma.info(f"[THEME] Loading theme: {named_style}")
        if name is None:
            name = generate_theme_name(palette)
        qss = join(here, "_data_", "themes", f"{named_style}.qss")
        logma.info(f"[THEME] QSS file path: {qss}")
        logma.info(f"[THEME] File exists: {exists(qss)}")

        # Read and log QSS content summary
        try:
            qss_content = open(qss, "r").read()
            logma.info(f"[THEME] QSS content length: {len(qss_content)} chars")
            # Check for any # references in the raw QSS
            hash_lines = [line for line in qss_content.split("\n") if "#" in line and "green" in line.lower()]
            if hash_lines:
                logma.info(f"[THEME] Lines with # and green: {hash_lines}")
        except Exception as e:
            logma.warning(f"[THEME] Could not read QSS: {e}")
            qss_content = ""

        if named_style == "dynamic":
            styled = self.create_theme(palette, name, qss_content)
            logma.info(f"[THEME] Dynamic theme created, length: {len(styled)}")
            self.app.setStyleSheet(styled)
        else:
            try:
                logma.info(f"[THEME] Setting stylesheet directly for: {named_style}")
                self.app.setStyleSheet(qss_content)
            except Exception as e:
                logma.warning(f"Could find style {named_style}")
                raise e
        self.app.setAutoFillBackground(True)

    def get_icon_path(self, name, icon_type="accent") -> None:
        """"""
        path = join(here, "_data_", "icons", self.iconset[icon_type], f"{name}.svg")
        if exists(path):
            return path
        path = join(here, "_data_", "icons", self.iconset[icon_type], f"dot-circle.svg")
        if exists(path):
            return path
        else:
            raise Exception(f"Icon doesnt exist {name}")

    def refocus_theme(self, focus) -> None:
        """"""
        # logma.info(f"FOCI {focus} {self.focus} {self.config.dikt.get('foci', 'blank')}")
        if focus not in self.config.dikt.get("foci", {}):
            raise Exception(f"Unknown focus {focus}")
        theme = self.config.dikt["foci"][focus]["theme"]
        if theme != self.theme:
            self.set_theme(theme)
        self.focus = focus
        return self

    def set_fonts(self) -> None:
        """"""
        self.small_font = pyqt.QFont("Arial", 8)
        self.medium_font = pyqt.QFont("Arial", 10)
        self.large_font = pyqt.QFont("Arial", 12)
        self.xlarge_font = pyqt.QFont("Arial", 14)
        return self

    def set_iconset(self, theme, palette) -> None:
        """"""
        self.iconset = self.config.dikt[theme]["iconset"][palette]
        if log:
            logma.info(f"Iconset {self.iconset}")
        return self

    def set_theme(self, theme, palette="primary") -> None:
        """"""
        self.theme = self.config.dikt[theme]
        self.palette = self.theme["palette"][palette]
        self.color = self.palette["color"]
        self.background = self.palette["background"]
        self.highlight = self.palette["highlight"]
        self.accent = self.palette["accent"]
        self.foreground = self.palette["foreground"]
        self.system = self.palette["system"]
        self.colors = {
            "accent": self.accent,
            "color": self.color,
            "highlight": self.highlight,
            "background": self.background,
            "foreground": self.foreground,
            "system": self.system,
        }
        self.import_theme(theme, palette)
        self.set_iconset(theme, palette)
        self.set_fonts()
        return self


def generate_theme_name(palette) -> None:
    """"""


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
