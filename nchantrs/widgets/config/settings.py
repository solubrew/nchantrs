from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.toolbars import NchantdButtonBar
from nchantrs.widgets.media.images import NchantdImage
from nchantrs.widgets.tabsets import NchantdTab
from nchantrs.widgets.config.config import NchantdConfigStoreDocument
from kahndor.logma import Logma
here = join(dirname(__file__), '')
logma = Logma(__name__)
logma.off()
pxcfg = join(here, '_data_', 'settings.yaml')

class NchantdSettingsWidget(NchantdTab):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdSettingsWidget').override(cfg))
        self.unsaved = False
        self.document = NchantdConfigStoreDocument()
        logma.info(f'NchantdSettingsWidget initialized')

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {'layout': 'horizontal', 'justify': 'right', 'size': ['auto', 50]}
        buttons = {0: {'action': 'show_pane_left', 'handler': self.cmd_show_pane_left}, 49: '_stretch', 100: {'action': 'save', 'handler': self.cmd_save}, 1000: {'action': 'show_pane_right', 'handler': self.cmd_show_pane_right}}
        self.button_bar = NchantdButtonBar(self, cfg).initWidget(buttons)
        self.button_bar.setFixedHeight(36)
        self.layout.addWidget(self.button_bar)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_export_file(self) -> None:
        logma.info(f'cmd_export_file invoked')
        return self

    def cmd_import_file(self) -> None:
        logma.info(f'cmd_import_file invoked')
        return self

    def cmd_save(self) -> None:
        logma.info(f'cmd_save invoked')
        return self

    def cmd_show_pane_left(self, event=None, *args, **kwargs) -> Any:
        """"""
        if self.app.view.panes['left'].isHidden():
            self.app.view.panes['left'].show()
        else:
            self.app.view.panes['left'].hide()
        return self

    def cmd_show_pane_right(self, event=None, *args, **kwargs) -> Any:
        """"""
        if self.app.view.panes['right'].isHidden():
            self.app.view.panes['right'].show()
        else:
            self.app.view.panes['right'].hide()
        return self

    def export_settings(self) -> None:
        logma.info(f'export_settings called')
        return self

    def get_settings(self, area) -> Any:
        """"""
        df = self.app.model.get_settings(area)
        return df

    def import_settings(self) -> None:
        logma.info(f'import_settings called')
        return self

    def launch_unsaved_dialog(self) -> None:
        logma.info(f'launch_unsaved_dialog called')
        return self

    def on_changed(self, value) -> None:
        """"""
        self.unsaved = True

    def onFocusOut(self) -> None:
        """"""
        super().onFocusOut()
        if self.unsaved:
            self.launch_unsaved_dialog()
            self.unsaved = False

    def save(self) -> None:
        """"""
        self.on_widget_changed()

    def set_defaults(self) -> None:
        """"""
        for setting in self.setting_configs:
            self.app.model.store_setting(setting)

class NchantdInterfaceSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdInterfaceSettingsTab').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdThemeSettings(NchantdSettingsWidget):
    """"""

    def __init__(self, parent, cfg=None) -> None:
        """"""
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdThemeSettingsTab').override(self.parent.config).override(cfg))
        self._load_themes()

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        self.config.dikt.pop('height', None)
        self.config.dikt.pop('width', None)
        darks = [x for x in self.themes.keys() if 'midnight' in x]
        lights = [x for x in self.themes.keys() if 'midday' in x]
        if len(self.themes.keys()) != 0:
            cfg = {'size': ['auto', 'auto']}
            dark_group = pyqt.QGroupBox()
            dark_group.setTitle('Themes')
            dark_group_layout = pyqt.QVBoxLayout()
            for theme in darks:
                if self.themes[theme]['active']:
                    cfg = {'size': ['auto', 'auto']}
                    theme_group = pyqt.QGroupBox()
                    theme_group.setTitle(self.themes[theme]['name'])
                    theme_group_layout = pyqt.QHBoxLayout()
                    theme_group.setLayout(theme_group_layout)
                    cfg = {'text': 'Set Active', 'handler': self.cmd_change_theme}
                    button = NchantdButton(self, cfg).initWidget()
                    theme_group_layout.addWidget(button)
                    color = self.themes[theme]['palette']['primary']['accent']
                    cfg = {'text': self.themes[theme]['name'], 'color': color, 'size': [150, 100]}
                    label = NchantdLabel(self, cfg).initWidget()
                    theme_group_layout.addWidget(label)
                    cfg = {'color': self.themes[theme]['palette']['primary']['accent'], 'size': [400, 100]}
                    image = NchantdImage(self, cfg).initWidget()
                    theme_group.setSizePolicy(pyqt.QSizePolicy.Policy.MinimumExpanding, pyqt.QSizePolicy.Policy.MinimumExpanding)
                    theme_group_layout.addWidget(image)
                    dark_group_layout.addWidget(theme_group)
            self.layout.addLayout(dark_group_layout)
            self.setSizePolicy(pyqt.QSizePolicy.Policy.Minimum, pyqt.QSizePolicy.Policy.Minimum)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def cmd_change_theme(self, event, *args, **kwargs) -> None:
        logma.info(f'cmd_change_theme invoked')
        return self

    def save(self) -> Any:
        """"""
        super().save()
        return self

    def _load_themes(self) -> Any:
        """"""
        self.themes = self.parent.app.view.themes
        return self