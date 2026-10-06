from typing import Any, Optional
from os.path import dirname, join

from kahndor import kahndor
from kahndor.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin

here = join(dirname(__file__), '')
logma = Logma(__name__)
log = True
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
        # Re-entrancy flag for on_index_change (pre-seeded so the
        # attribute exists before init_triggers connects signals).
        self._in_index_change = False

    def initModel(self, handler=None) -> Any:
        """"""
        self.init_variables()
        self.setEditable(True)
        self.set_options(self.config.get('options', []), self.config.get('sort', True))
        self.lineEdit().setPlaceholderText('Type or select an item')
        value = self.config.get('value', None)
        if value is None:
            value = ""
        if not isinstance(value, str):
            logma.info(f"Type {type(value)}")
            raise Exception(f"Assigned Value Type Incorrect")
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
        # NoInsert: on Enter, Qt must NOT auto-insert the typed text.
        # InsertAtTop inserted it at index 0, which SHIFTED the
        # previously-current item to index 1 and fired a spurious
        # currentIndexChanged(1) -> on_index_change, which then
        # reset the line edit back to that shifted item (the old
        # URL) and navigated there — i.e. Enter "defaulted back to
        # the original". With NoInsert no such signal fires; Enter
        # navigation is driven explicitly from on_return_pressed
        # using the actual line-edit text.
        self.setInsertPolicy(pyqt.QComboBox.NoInsert)
        # Drop the inline autocompleter. It was silently rewriting
        # the user's partial text to a matching existing item (a
        # typed prefix became 'https://www.pyffice.com/'), so Enter
        # matched an existing item and navigated to that URL instead
        # of the manually-typed one. Removing it preserves manual
        # input verbatim; the dropdown history is still selectable.
        self.setCompleter(None)
        self.set_size()
        return self

    def init_triggers(self) -> Any:
        """"""
        self.lineEdit().returnPressed.connect(self.on_return_pressed)
        # T-NEW-071 — handler set on the instance takes
        # precedence over config.dikt.get('handler'). Buttons
        # pass handlers via __init__/initWidget; the previous
        # unconditional overwrite silently dropped navigation
        # events on the Enter path. Mirror the
        # `_in_index_change` / `options` guard style.
        if self.handler is None:
            self.handler = self.config.get('handler', None)
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
        """Current entry = whatever the line edit shows.

        Deliberately NOT ``self.value or currentText()``: ``self.value``
        is only refreshed by the signal handlers, so it goes stale
        when the user types a new URL and clicks the Go button
        without pressing Enter — get_value would then return the
        previously-navigated URL instead of what's typed.
        """
        return self.currentText()

    def toggle_editable(self) -> Any:
        """"""
        if self.isEditable():
            self.setEditable(False)
            return self
        self.setEditable(True)
        return self

    def on_activated(self, index) -> None:
        """Fires when the user picks an item from the dropdown popup.

        Navigation for a pick is handled by ``on_index_change``
        (currentIndexChanged fires alongside activated), and Enter
        on typed text is handled by ``on_return_pressed``. With the
        ``NoInsert`` policy Qt never emits ``activated(-1)`` for new
        text, so there is nothing to commit here — this is
        informational only.
        """
        logma.info(f"Activated Index {index}")
        logma.info(f"Activated Text {self.lineEdit().text().strip()}")

    def on_index_change(self, index) -> None:
        """
        Fires on every currentIndexChanged — INCLUDING the
        synthetic index ``-1`` emitted while the combobox is
        being programmatically cleared/repopulated (dropdown
        history sync in ``set_url_path``). Guard:

        1. index -1 (mid-repopulation) must NOT call the
           handler — the old code forwarded it, producing
           ``cmd_goto_page(-1)`` -> ``goto_page(None)`` ->
           ``set_url_path`` -> ``update_options(replace=True)``
           -> ``combobox.clear()`` -> currentIndexChanged(-1)
           -> ... infinite ping-pong (surfaced as
           RecursionError inside the logging formatter).
        2. Re-entrancy guard: if the handler itself mutates
           the dropdown (it does — URL tracking updates
           options), the nested signal is dropped.

        :param index:
        :return:
        """
        if index is None or index < 0:
            return
        if getattr(self, "_in_index_change", False):
            return
        self._in_index_change = True
        try:
            self.value = self.itemText(index)
            self.setCurrentText(self.value)
            if self.handler is not None:
                logma.info(f'Handler {self.handler}')
                self.handler(index, self.itemText(index))
        finally:
            self._in_index_change = False
        return

    def on_return_pressed(self) -> Any:
        """Enter on the URL bar — the single navigation path.

        With ``NoInsert`` (see initView) Qt fires no
        activated/currentIndexChanged on Enter, so this is the
        deterministic place to commit a manually-typed entry.
        We read the *actual* line-edit text (immune to the
        index-shift clobber that InsertAtTop caused), register it
        as an option + active value, and invoke the handler so
        Enter navigates to exactly what was typed. Picks from the
        dropdown popup still go through on_index_change.
        """
        text = self.lineEdit().text().strip()
        if not text:
            return self
        # All widget mutations under a signal blocker: addItem on an
        # empty combobox, and setCurrentIndex, would otherwise fire
        # currentIndexChanged -> on_index_change and re-enter the
        # handler. We call the handler ourselves once, below.
        with pyqt.QSignalBlocker(self):
            existing = self.findText(text)
            if existing == -1:
                self.addItem(text)
                existing = self.findText(text)
            self.setCurrentIndex(existing)
            self.setCurrentText(text)
        # Keep the tracked option list(s) in sync with the widget so
        # a manual entry survives a later replace/repopulate and is
        # counted in set_size (mirrors the parent NchantdDropDown).
        if text not in self.options:
            self.options.append(text)
        parent = getattr(self, 'parent', None)
        if parent is not None and hasattr(parent, 'options') \
                and text not in parent.options:
            parent.options.append(text)
        self.value = text
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        if self.handler is not None:
            logma.info(f'Handler {self.handler}')
            try:
                self.handler(existing, text)
            except Exception as _exc:
                logma.error(
                    f'handler error in on_return_pressed for {text!r}: {_exc}'
                )
        return self

    def on_text_change(self) -> Any:
        logma.info('on_text_change event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def on_text_edit(self, event, *args, **kwargs) -> Any:
        logma.info('on_text_edit event received')
        if getattr(self, 'app', None) is not None and hasattr(self.app, 'model'):
            self.app.model.has_changed = True
        return self

    def set_current_text(self) -> Any:
        logma.info('set_current_text called')
        if hasattr(self, 'current_text'):
            logma.info('  has current_text attr')
        return self

    def set_size(self) -> None:
        """"""
        min_width_min = None
        min_height_min = None
        if self.config.get('size', None) is None:
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
        # Programmatic clear+repopulate must NOT fire
        # currentIndexChanged — the -1/-0 pairs emitted here
        # would re-enter the URL handler loop (RecursionError).
        # QSignalBlocker suppresses them for the scope.
        with pyqt.QSignalBlocker(self):
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
        self.options = self.config.get('options', [])
        return self

    def initView(self, handler=None) -> Any:
        """Build the dropdown view: a label above the combobox."""
        cfg = {}
        super().initView(cfg)
        logma.info(f"Label {self.config.get('label', 'Missing Label')}")
        self.config.dikt['label'] = self.config.get('label', 'Missing Label')
        self.label = NchantdLabel(self, self.config).initWidget()
        self.layout.setAlignment(self.label, pyqt.Qt.AlignTop | pyqt.Qt.AlignLeft)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        cfg = self.config.get('combobox')
        logma.info(f'{cfg}')
        self.combobox = NchantdComboBox(self, cfg).initWidget(handler)
        self.update_options(self.options, False, self.config.get('sort', True))
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
        logma.info('on_return_pressed event received')
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
            # Block signals during the clear: combobox.clear()
            # emits currentIndexChanged(-1) which would re-enter
            # the handler loop (T-NEW-069 RecursionError).
            combobox = getattr(self, 'combobox', None)
            if combobox is not None:
                with pyqt.QSignalBlocker(combobox):
                    combobox.clear()
            else:
                pass  # combobox not built yet — nothing to clear
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
        cfg = {'action': self.config.get('action', {})}
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
        logma.info('NchantdDropDownExplainer initialized')

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
