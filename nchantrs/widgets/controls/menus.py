from typing import Any
'\n---\n<(META)>:\n        docid:\n        name:\n        description: >\n        version: 0.0.0.0.0.0\n        authority: filesystem\n        security: seclvl2\n        <(WT)>: -32\n'
from os.path import abspath, dirname, join
from kahndor import kahndor
from nchantrs.utilities.utils import convert_df_to_tree, lookup
from nchantrs.libraries import pyqt
from kahndor.logma import Logma
here = join(dirname(__file__), '')
logma = Logma(__name__)
log = False
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'menus.yaml')

class NchantdMenu(pyqt.QMenu):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdMenu').override(parent.config).override(cfg)
        self.actions = None
        self.menus = {}

    def initModel(self) -> Any:
        """ """
        self.actions = self.config.dikt.get('actions', [])
        return self

    def initView(self) -> Any:
        """ """
        for action in self.actions:
            if isinstance(action, str):
                action = lookup(self.parent, action, None, True, True, False)
            elif isinstance(action, int):
                action = lookup(self.parent, action, None, True, True, False)
            self.add_action(action.get('name_txt', None), action.get('handler', None))
        return self

    def initWidget(self) -> Any:
        super_method = getattr(super(type(self), self), method_name, None)
        if callable(super_method):
            try:
                super_method()
            except TypeError:
                pass
        logma.info(f'initWidget {{type(self).__name__}}')
        return self

    def add_action(self, title, handler) -> Any:
        """"""
        action = pyqt.QAction(title, self)
        if handler is not None and handler != '':
            handler = getattr(self.parent, handler)
            action.triggered.connect(handler)
        self.addAction(action)
        return self

    def buildMenu(self, menu=None, menus=None) -> Any:
        """Build menu from menu configuration tree"""
        if menus is None:
            return self
        for code, subcode in menus.items():
            logma.info(f'Code {code} Subcode {subcode}')
            logma.info(f'Menus {self.menus}')
            menu_cfg = self.menu_df[self.menu_df['name_txt'] == code].to_dict('records')[0]
            logma.info(f'Menu {menu_cfg}')
            if menu_cfg['name_txt'] is None:
                menu_cfg['name_txt'] = code
            if menu not in self.menus:
                self.menus[menu] = self.addMenu(f"{menu_cfg['name_txt']}")
            self.menus[code] = self.menus[menu].addMenu(f"{menu_cfg['name_txt']}")
            if subcode is not None and (not subcode == {}):
                self.buildMenu(code, subcode)
            else:
                logma.info(f"Action {menu_cfg['name_txt']} {menu_cfg['handler']}")
                if menu_cfg['handler'] is None or menu_cfg['handler'] == '':
                    continue
                if hasattr(self.parent, menu_cfg.get('handler', None)):
                    self.add_action(menu_cfg['name_txt'], getattr(self.parent, menu_cfg['handler']))
        return self

class NchantdContextMenu(NchantdMenu):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdContextMenu').override(cfg))
        self.menu_data = None
        self.name = None
        self.menu_df = None

    def initModel(self) -> Any:
        """"""
        super().initModel()
        self.name = self.config.dikt.get('name', None)
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        self.buildMenu(self.name, self.menu_data)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def get_menu(self, name=None) -> Any:
        """"""
        logma.info(f'Name {name}')
        if name:
            self.name = name
        self.menu_df = self.parent.app.model.get_menu(self.name)
        logma.info(f'Menu Data {self.menu_df.head()}')
        menu_data = convert_df_to_tree(self.menu_df)
        logma.info(f'Menu Data {menu_data}')
        if self.menu_data is None:
            self.menu_data = menu_data
        else:
            self.menu_data.update(menu_data)
        logma.info(f'Menu Data {self.menu_data.keys()}')
        self.buildMenu(self.name, self.menu_data)
        return self

    def invalidate_cache(self, name=None) -> Any:
        """Invalidate the application-wide menu cache.

        Delegates to the model so every menu/widget sees the refresh. Pass a
        name to drop a single cached menu, or omit it to clear them all. Call
        this whenever the underlying menu data changes.
        """
        self.parent.app.model.invalidate_menu_cache(name)
        return self