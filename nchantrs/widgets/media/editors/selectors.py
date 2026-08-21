from typing import Any, Optional
'\n---\n<(META)>:\n    docid:\n    name:\n    description: >\n    version: 0.0.0.0.0.0\n    authority: filesystem\n    security: seclvl2\n    <(WT)>: -32\n'
from os.path import dirname, join
from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
here = join(dirname(__file__), '')
logma = Logma(__name__)
log = False
if not log:
    logma.off()
pxcfg = join(here, '_data_', 'selectors.yaml')

class NchantdComboBox(NchantdWidgetMixin, pyqt.QComboBox):
    """ """

    def __init__(self, parent=None, cfg=None, *args, **kwargs) -> None:
        """ """
        super().__init__()
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('NchantdComboBox').override(parent.config).override(cfg)
        self.handler = None
        self.value = None
        self.options = []

    def initModel(self, handler=None) -> Any:
        """"""
        self.init_variables()
        self.setEditable(True)
        self.set_options(self.config.dikt.get('options', []), self.config.dikt.get('sort', True))
        self.lineEdit().setPlaceholderText('Type or select an item')
        value = self.config.dikt.get('value', None)
        logma.info(f'Value {value}')
        if value not in self.options:
            self.add_option(value)
        if value is not None and value in self.options:
            self.set_value(value)
        elif value is None and len(self.options) > 0:
            self.set_value(self.options[0])
        self.init_triggers()
        return self

    def initView(self) -> Any:
        """"""
        self.setInsertPolicy(pyqt.QComboBox.InsertAtTop)
        self.set_size()
        return self

    def init_triggers(self) -> Any:
        """"""
        self.lineEdit().returnPressed.connect(self.on_return_pressed)
        self.handler = self.config.dikt.get('handler', None)
        self.activated.connect(self.on_activated)
        self.currentIndexChanged.connect(self.on_index_change)
        self.currentTextChanged.connect(self.on_text_change)
        self.editTextChanged.connect(self.on_text_edit)
        return self

    def initWidget(self, handler=None) -> Any:
        """

        :param handler:
        :return:
        """
        self.initModel(handler)
        self.initView()
        return self

    def add_option(self, option) -> Any:
        """"""
        logma.info(f'Option {option}')
        self.addItem(option)
        return self

    def get_value(self) -> Any:
        """"""
        return self.currentText()

    def toggle_editable(self) -> Any:
        """"""
        if self.isEditable():
            self.setEditable(False)
            return self
        self.setEditable(True)
        return self

    def on_activated(self, index) -> None:
        """"""
        if index == -1:
            text = self.lineEdit().text().strip()
            if text:
                self.addItem(text)
                self.setCurrentIndex(self.findText(text))
                self.lineEdit().clear()

    def on_index_change(self, index) -> None:
        """
        :param index:
        :return:
        """
        self.value = self.itemText(index)
        self.setCurrentText(self.value)
        if index is not None and self.handler is not None:
            logma.info(f'Handler {self.handler}')
            self.handler(index, self.itemText(index))
        return

    def on_return_pressed(self) -> Any:
        logma.info(f'on_return_pressed event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def on_text_change(self) -> Any:
        logma.info(f'on_text_change event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def on_text_edit(self, event, *args, **kwargs) -> Any:
        logma.info(f'on_text_edit event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def set_current_text(self) -> Any:
        logma.info(f'set_current_text called')
        if hasattr(self, 'current_text'):
            logma.info(f'  has current_text attr')
        return self

    def set_size(self) -> None:
        """"""
        min_width_min = None
        min_height_min = None
        if self.config.dikt.get('size', None) is None:
            max_width = 500
            min_width_min = 50
            min_height_min = 20
            for option in self.options:
                text_width, text_height = self._get_text_size(str(option))
                min_width, min_height = (text_width + 30, text_height)
                if min_width > min_width_min:
                    min_width_min = min_width
                if min_height > min_height_min:
                    min_height_min = min_height
            if min_width_min > max_width:
                min_width_min = max_width
        self.setMaximumWidth(150)
        super().set_size(min_width_min, min_height_min, None, 30)

    def set_value(self, text) -> Any:
        """"""
        self.setCurrentIndex(self.findText(text))
        return self

    def set_options(self, options, sort=None) -> Any:
        """Set the dropdown's options and optionally sort them.

        :param options: List of options to display.  Each entry can be
            a string or a dict with a 'name' key (the value is the 'name').
        :param sort: Sort strategy.  None / 'alpha' (default) sorts
            alphabetically.  'insertion' preserves the input order.
            'value' co-erces to float before sorting (numeric ascending).
        :return: self
        """
        if sort is None:
            sort = 'alpha'
        if options is None or options == []:
            return
        logma.info(f'Options {options}')
        if isinstance(options[0], dict):
            self.options = [x['name'] for x in options]
        else:
            self.options = options
        self.options = [x for x in self.options if x is not None]
        if sort == 'insertion':
            pass  # preserve input order
        elif sort == 'value':
            try:
                self.options = sorted(self.options, key=lambda x: float(x))
            except (ValueError, TypeError):
                self.options.sort()
        else:  # 'alpha' or unknown
            self.options.sort()
        self.options = [str(x) for x in self.options]
        logma.info(f'Options {self.options}')
        self.clear()
        self.addItems(self.options)
        return self

class NchantdDropDown(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdDropDown').override(cfg))
        self.combobox = None
        self.options = []

    def initModel(self, handler) -> Any:
        """
        :param handler:
        :return:
        """
        super().initModel()
        self.options = self.config.dikt.get('options', [])
        return self

    def initView(self, handler=None) -> Any:
        """Build the dropdown view: a label above the combobox."""
        cfg = {}
        super().initView(cfg)
        logma.info(f"Label {self.config.dikt.get('label', 'Missing Label')}")
        self.config.dikt['label'] = self.config.dikt.get('label', 'Missing Label')
        self.label = NchantdLabel(self, self.config).initWidget()
        self.layout.setAlignment(self.label, pyqt.Qt.AlignTop | pyqt.Qt.AlignLeft)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        cfg = self.config.dikt.get('combobox')
        logma.info(f'{cfg}')
        self.combobox = NchantdComboBox(self, cfg).initWidget(handler)
        self.update_options(self.options, False, self.config.dikt.get('sort', True))
        self.layout.setAlignment(self.combobox, pyqt.Qt.AlignTop | pyqt.Qt.AlignLeft)
        self.layout.addWidget(self.combobox)
        return self

    def initWidget(self, handler=None) -> Any:
        """ """
        self.initModel(handler)
        self.initView(handler)
        return self

    def get_value(self) -> Optional[Any]:
        """"""
        if self.combobox is None:
            return None
        return self.combobox.get_value()

    def on_return_pressed(self, method) -> Any:
        logma.info(f'on_return_pressed event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def set_option_selection(self, value) -> Any:
        """"""
        logma.info(f'Option Selection {value}')
        if value is None:
            value = self.options[0]
        self.combobox.setCurrentIndex(self.combobox.findText(value))
        return self

    def set_options(self, options) -> None:
        """"""
        self.update_options(options, True)

    def  set_value(self, value):
        """"""
        if self.combobox is None:
            return None
        self.combobox.set_value(value)
        return self

    def update_options(self, options, replace=False, sort=None) -> Any:
        """Add or replace the dropdown's options.

        :param options: list of options (or a single option).  None entries
            are skipped.
        :param replace: when True, clear the existing options first.
        :param sort: sort strategy forwarded to ``self.combobox.set_options``.
            None / 'alpha' sorts alphabetically; 'insertion' preserves
            input order; 'value' sorts numerically.
        :return: self
        """
        if sort is None:
            sort = True
        if not isinstance(options, list):
            options = [options]
        if replace:
            self.options = []
            self.combobox.clear()
        self.options += options
        for x in self.options:
            if x is None:
                continue
            if replace:
                self.combobox.set_options(self.options, sort=sort)
            elif self.combobox.findText(x) == -1:
                self.combobox.addItem(x)
        return self

class NchantdDropDownActivator(NchantdDropDown):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdDropDownActivator').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfg = {'action': self.config.dikt.get('action', {})}
        self.activate_button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.activate_button)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdDropDownExplainer(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        self.parent = parent
        self.config = kahndor.Instruct(pxcfg).select('Nchantd')
        if self.parent:
            self.config.override(parent.config)
        super().__init__(self)
        self.config.override(cfg)
        self.explainer = None
        logma.info(f'NchantdDropDownExplainer initialized')

    def initModel(self) -> Any:
        """"""
        super().initModel()
        return self

    def initView(self) -> Any:
        """"""
        super().initView({'layout': 'vertical'})
        cfg = self.config.override({'layout': 'horizontal'}).dikt
        self.dropdown = NchantdDropDown(self, cfg).initWidget()
        self.layout.addWidget(self.dropdown)
        self.update_explainer()
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

    def update_explainer(self) -> Any:
        """"""
        if self.explainer is not None:
            self.layout.removeWidget(self.explainer)
            self.explainer.setParent(None)
        self.explainer = NchantdLabel(self, self.config.override({}).dikt).initWidget()
        self.layout.addWidget(self.explainer)
        return self

class NchantdCheckboxCombo(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdCheckboxCombo').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self) -> Any:
        """"""
        super().initView()
        cfg = {}
        self.checkbox = NchantdCheckbox(self, cfg).initWidget()
        self.layout.addWidget(self.checkbox)
        cfg = {}
        self.combobox = NchantdComboBox(self, cfg).initWidget()
        self.layout.addWidget(self.combobox)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self

class NchantdComboEditor(NchantdWidget):
    """"""

    def __init__(self, parent=None, cfg=None) -> None:
        """ """
        super().__init__(parent, cfg)
        self.config.override(kahndor.Instruct(pxcfg).select('NchantdComboEditor').override(cfg))

    def initModel(self, cfg=None) -> Any:
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None) -> Any:
        """"""
        super().initView(cfg)
        cfgt = {}
        self.combobox = NchantdComboBox(self, cfg).initWidget()
        self.layout.addWidget(self.combobox)
        self.entry = NchantdEntryBox(self, cfgt).initWidget()
        self.layout.addWidget(self.entry)
        return self

    def initWidget(self) -> Any:
        """"""
        self.initModel()
        self.initView()
        return self