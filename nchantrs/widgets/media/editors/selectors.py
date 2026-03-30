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

import logging
# ======================================3rd Party Library Modules=====================================================||

logger = logging.getLogger(__name__)

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma
from nchantrs.libraries import pyqt
from nchantrs.widgets.annotations import NchantdLabel
from nchantrs.widgets.media.editors.editors import NchantdEntryBox
from nchantrs.widgets.controls.buttons import NchantdButton
from nchantrs.widgets.controls.checkboxes import NchantdCheckbox
from nchantrs.widgets.widgets import NchantdWidget, NchantdWidgetMixin
# ====================================================================================================================||
here = join(dirname(__file__), '')  # ||
logma = Logma(__name__)
logma.off()

# ====================================================================================================================||
pxcfg = join(here, '_data_', 'selectors.yaml')



class NchantdComboBox(NchantdWidgetMixin, pyqt.QComboBox):
    """ """

    def __init__(self, parent=None, cfg=None, *args, **kwargs):
        """ """
        super().__init__()
        self.parent = parent
        self.config = condor.Instruct(pxcfg).select("NchantdComboBox")
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.handler = None
        self.value = None
        self.options = []

    def initModel(self, handler=None):
        """"""
        self.init_variables()
        self.setEditable(True)  # Set up the completer
        self.set_options(self.config.dikt.get("options", []), self.config.dikt.get("sort", True))
        self.lineEdit().setPlaceholderText("Type or select an item")  # Create a custom widget for editing
        value = self.config.dikt.get("value", None)
        logma.info(f"Value {value}")
        if value not in self.options:
            self.add_option(value)
        if value is not None and value in self.options:
            self.set_value(value)
        elif value is None and len(self.options) > 0:
            self.set_value(self.options[0])
        self.init_triggers()
        return self

    def initView(self):
        """"""
        self.setInsertPolicy(pyqt.QComboBox.InsertAtTop)
        # # TODO replace with size methods from NchantdWidgetMixin
        self.set_size()
        return self

    def init_triggers(self):
        """"""
        self.lineEdit().returnPressed.connect(self.on_return_pressed)
        self.handler = self.config.dikt.get("handler", None)
        self.activated.connect(self.on_activated)
        self.currentIndexChanged.connect(self.on_index_change)
        self.currentTextChanged.connect(self.on_text_change)
        self.editTextChanged.connect(self.on_text_edit)
        return self

    def initWidget(self, handler=None):
        """

        :param handler:
        :return:
        """
        self.initModel(handler)
        self.initView()
        return self

    def add_option(self, option):
        """"""
        self.addItem(option)
        return self

    def get_value(self):
        """"""
        return self.currentText()

    def toggle_editable(self):
        """"""
        if self.isEditable():
            self.setEditable(False)
            return self
        self.setEditable(True)
        return self

    def on_activated(self, index):
        """"""
        # Handle item selection
        if index == -1:  # -1 means the entered text is not in the list
            text = self.lineEdit().text().strip()
            if text:
                self.addItem(text)
                self.setCurrentIndex(self.findText(text))
                self.lineEdit().clear()

    def on_index_change(self, index):
        """
        :param index:
        :return:
        """
        self.value = self.itemText(index)
        self.setCurrentText(self.value)
        if index is not None and self.handler is not None:
            logma.info(f"Handler {self.handler}")
            self.handler(index, self.itemText(index))
        return

    def on_return_pressed(self):
        """"""
        #commented out to fix issue with NchantdWebViewer url drop down not sure if it will be an issue else where
        # Handle the return/enter key press
        # logma.on()
        # logma.info(f"Return Pressed")
        # text = self.lineEdit().text().strip()
        # logma.info(f"Text {text}")
        # if text:
        #     self.addItem(text)
        #     self.setCurrentIndex(self.findText(text))
        #     self.lineEdit().clear()
        # logma.off()
        return self
    def on_text_change(self):
        """"""
        return self

    def on_text_edit(self, event, *args, **kwargs):
        """"""
        return self

    def set_current_text(self):
        """"""

        return self

    def set_size(self):
        """"""
        min_width_min = None
        min_height_min = None
        if self.config.dikt.get("size", None) is None:
            max_width = 500
            min_width_min = 50
            min_height_min = 20
            for option in self.options:
                text_width, text_height = self._get_text_size(str(option))
                min_width, min_height = text_width + 30, text_height
                if min_width > min_width_min:
                    min_width_min = min_width
                if min_height > min_height_min:
                    min_height_min = min_height
            if min_width_min > max_width:
                min_width_min = max_width
            # self.setFixedWidth(min_width_min + 40)
            # self.setMinimumHeight(min_height_min)
        super().set_size(min_width_min, min_height_min, None, 30)

    def set_value(self, text):
        """"""
        self.setCurrentIndex(self.findText(text))
        return self

    def set_options(self, options, sort=True):
        """
        #TODO implement a more sophisticated sorting mechanism to allow control of options display
        :param options:
        :param sort:
        :return:
        """
        # logma.info(f"Options {options}")
        if options is None or options == []:
            return
        logma.info(f"Options {options}")
        if isinstance(options[0], dict):
            self.options = [x["name"] for x in options]  # + self.config.dikt.get("default", [])
        else:
            self.options = options
        self.options = [x for x in self.options if x is not None]
        #if sort:
        #TODO: should always be sorted in some positive manner either by the values or a given sequence
        logma.info(f"Options {self.options}")
        self.options = list(set(self.options))
        self.options.sort()
        self.options = [str(x) for x in self.options]
        logma.info(f"Options {self.options}")
        self.clear()
        self.addItems(self.options)
        return self


class NchantdDropDown(NchantdWidget):
    """ """

    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(parent, cfg)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select("NchantdDropDown"))
        if parent:
            self.config.override(parent.config)
        self.config.override(cfg)
        self.label = None
        self.combobox = None
        self.options = []

    def initModel(self, handler):
        """
        :param handler:
        :return:
        """
        super().initModel()
        self.options = self.config.dikt.get("options", [])
        return self

    def initView(self, handler=None):
        """ """
        super().initView()
        logma.info(f"Label {self.config.dikt.get('label', 'Missing Label')}")
        self.config.dikt["label"] = self.config.dikt.get("label", "Missing Label")
        self.label = NchantdLabel(self, self.config).initWidget()
        self.layout.setAlignment(self.label, pyqt.Qt.AlignTop | pyqt.Qt.AlignLeft)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        cfg = self.config.dikt.get("combobox")
        logma.info(f"{cfg}")
        self.combobox = NchantdComboBox(self, cfg).initWidget(handler)
        self.update_options(self.options, False, self.config.dikt.get("sort", True))
        self.layout.setAlignment(self.combobox, pyqt.Qt.AlignTop | pyqt.Qt.AlignLeft)
        self.layout.addWidget(self.combobox)
        return self

    def initWidget(self, handler=None):
        """ """
        self.initModel(handler)
        self.initView(handler)
        return self

    def get_value(self):
        """"""
        return self.combobox.get_value()

    def on_return_pressed(self, method):
        """"""
        return self

    def set_option_selection(self, value):
        """"""
        logma.info(f"Option Selection {value}")
        if value is None:
            value = self.options[0]
        self.combobox.setCurrentIndex(self.combobox.findText(value))
        return self

    def update_options(self, options, replace=False, sort=True):
        """"""
        if not isinstance(options, list):
            options = [options]
        if replace:
            self.options = []
        self.options += options
        options = []
        for x in self.options:
            if x is None:
                continue
            options.append(x)
            if self.combobox.findText(x) == -1:  # -1 means the item doesn't exist
                self.combobox.addItem(x)
        return self


class NchantdDropDownActivator(NchantdDropDown):
    """"""
    def __init__(self, parent=None, cfg=None):
        """ """
        super().__init__(self)
        self.parent = parent
        self.config.override(condor.Instruct(pxcfg).select('NchantdDropDownActivator'))
        if self.parent:
            self.config.override(parent.config)
        self.config.override(cfg)

    def initModel(self, cfg=None):
        """"""
        super().initModel(cfg)
        return self

    def initView(self, cfg=None):
        """"""
        super().initView(cfg)
        cfg = {"action": self.config.dikt.get("action", {})}
        self.activate_button = NchantdButton(self, cfg).initWidget()
        self.layout.addWidget(self.activate_button)
        return self

    def initWidget(self):
        """"""
        self.initModel()
        self.initView()
        return self

#
# class NchantdDropDownActivator(NchantdWidget):
# 	""""""
# 	def __init__(self, parent=None, cfg=None):
# 		""" """
# 		self.parent = parent
# 		self.config = condor.Instruct(pxcfg).select('Nchantd')
# 		if self.parent:
# 			self.config.override(parent.config)
# 		super().__init__(self)
# 		self.config.override(cfg)
#
# 	def initModel(self):
# 		""""""
# 		super().initModel()
# 		return self
#
# 	def initView(self):
# 		""""""
# 		super().initView()
# 		return self
#
# 	def initWidget(self):
# 		""""""
# 		self.initModel()
# 		self.initView()
# 		return self
#

class NchantdDropDownExplainer(NchantdWidget):
	""""""
	def __init__(self, parent=None, cfg=None):
		""" """
		self.parent = parent
		self.config = condor.Instruct(pxcfg).select('Nchantd')
		if self.parent:
			self.config.override(parent.config)
		super().__init__(self)
		self.config.override(cfg)
		self.explainer = None

	def initModel(self):
		""""""
		super().initModel()
		return self

	def initView(self):
		""""""
		super().initView({"layout": "vertical"})
		cfg = self.config.override({"layout": "horizontal"}).dikt
		self.dropdown = NchantdDropDown(self, cfg).initWidget()
		self.layout.addWidget(self.dropdown)
		self.update_explainer()
		return self

	def initWidget(self):
		""""""
		self.initModel()
		self.initView()
		return self

	def update_explainer(self):
		""""""
		if self.explainer is not None:
			self.layout.removeWidget(self.explainer)
			self.explainer.setParent(None)
		self.explainer = NchantdLabel(self, self.config.override({}).dikt).initWidget()
		self.layout.addWidget(self.explainer)
		return self


class NchantdCheckboxCombo(NchantdWidget):
	""""""
	def __init__(self, parent=None, cfg=None):
		""" """
		self.parent = parent
		self.config = condor.Instruct(pxcfg).select('Nchantd')
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
		cfg = {}
		self.checkbox = NchantdCheckbox(self, cfg).initWidget()
		self.layout.addWidget(self.checkbox)
		cfg = {}
		self.combobox = NchantdComboBox(self, cfg).initWidget()
		self.layout.addWidget(self.combobox)
		return self

	def initWidget(self):
		""""""
		self.initModel()
		self.initView()
		return self


class NchantdComboEditor(NchantdWidget):
	""""""
	def __init__(self, parent=None, cfg=None):
		""" """
		super().__init__(parent, cfg)
		self.parent = parent
		self.config.override(condor.Instruct(pxcfg).select('NchantdComboEditor'))
		if self.parent:
			self.config.override(parent.config)
		self.config.override(cfg)

	def initModel(self, cfg=None):
		""""""
		super().initModel(cfg)
		return self

	def initView(self, cfg=None):
		""""""
		super().initView(cfg)
		cfgt = {}
		self.combobox = NchantdComboBox(self, cfg).initWidget()
		self.layout.addWidget(self.combobox)
		self.entry = NchantdEntryBox(self, cfgt).initWidget()
		self.layout.addWidget(self.entry)
		return self

	def initWidget(self):
		""""""
		self.initModel()
		self.initView()
		return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
