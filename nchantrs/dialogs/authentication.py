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
# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.widgets.widgets import NchantdWidget
# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class NchantdAuthenticationWindow(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("NchantdAuthenticationWindow").override(cfg))

    def initModel(self, cfg=None) -> None:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> None:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> None:
        """"""
        self.initModel()
        self.initView()
        return self


# # You might want to create a dialog for the popup
# from PySide6.QtWidgets import QDialog
#
# popup_dialog = QDialog(self)
# popup_dialog.setWindowTitle("Google Authentication")
# popup_dialog.resize(500, 600)
#
# popup_layout = QVBoxLayout(popup_dialog)
# popup_view = QWebEngineView(popup_dialog)
# popup_view.setPage(popup_page)
# popup_layout.addWidget(popup_view)
#
# # Show popup
# popup_dialog.show()
#
# # Monitor for completion
# popup_page.urlChanged.connect(lambda url: self.check_auth_completion(url, popup_dialog))
#
#
# def handle_new_window(self, request) -> None:
#     """Handle new window requests (like OAuth popups)."""
#     # Create new page for popup
#     popup_page = QWebEnginePage(self.session_manager.profile, self)
#     popup_page.setUrl(request.requestedUrl())


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
