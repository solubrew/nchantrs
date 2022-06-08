#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	docid:   #																	||
	name:   #																	||
	description: >  #															||
		  #			||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from os.path import abspath, dirname, join
#===============================================================================||
from condor import condor
from nchantrs.libraries import pyqt
from nchantrs.widgets import annotations
#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
log = True
#===============================================================================||
pxcfg = join(abspath(here), f'_data_/controls.yaml')

class NchantdButton(pyqt.QPushButton):
	''' '''

	def __init__(self, parent=None, cfg={}):
		'''Create a button widget and set default configurations'''
		self.config = condor.instruct(pxcfg)
		self.config.select('NchantdButton')
		if log: print('CONFIG\n', self.config.dikt)
		if log: print('CFG\n', cfg)
		self.config.override(cfg)
		if log: print('Override CONFIG\n', self.config.dikt)
		if parent:
			self.config.override(parent.config)
		if log: print('Parent Override Config\n', self.config.dikt)
		super(NchantdButton, self).__init__()

	def initWidget(self):
		''' '''
		self.setCheckable(self.config.dikt['checkable'])
		if self.config.dikt['icon']:
			self.setIcon(pyqt.QIcon(self.config.dikt['icon']))
		self.setEnabled(self.config.dikt['enabled'])
		if log: print('Button Text\n', self.config.dikt['text'])
		self.setText(self.config.dikt['text'])
		self.setAutoDefault(self.config.dikt['auto_default'])
		self.setEnabled(self.config.dikt['enabled'])
		# handler = self.config.dikt['handlers']['clicked_handler']
		# if handler:
		# 	self.clicked.connect(getattr(parent, handler))


class NchantdCheckbox(pyqt.QCheckBox):
	def __init__(self, app, cfg={}, parent=None):
		'''https://www.tutorialspoint.com/pyqt/pyqt_qcheckbox_self.htm '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).select('nchantdbutton')
		self.config.override(cfg)
		self.config.dikt['text'] = cfg['text']#override bug
		if log: print('Nchantd Button Config\n', self.config.dikt)
		super(NchantdCheckbox, self).__init__(cfg['name'], parent)
		self.setText(cfg['text'])
		self.setChecked(cfg['checked'])
		self.stateChanged.connect(getattr(app, cfg['handlers']['stateChanged_handler']))
		self.toggled.connect(getattr(app, cfg['handlers']['toggled_handler']))
		return widget


class NchantdComboBox(pyqt.QComboBox):
	''' '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdComboBox')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdComboBox, self).__init__()
		self.addItems(self.config.dikt['default_items'])
#		self.activated.connect(getattr(self, self.config.dikt['handlers']['activated_handler']))
#		self.currentIndexChanged.connect(getattr(self, self.config.dikt['handlers']['current_index_changed_handler']))
#		self.highlight.connect(getattr(self, self.config.dikt['handlers']['highlighted_handler']))


class NchantdDropDown(pyqt.QWidget):
	''' '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdDropDown')
		self.config.override(cfg)
		if parent:
			self.config.override(parent.config)
		super(NchantdDropDown, self).__init__()
	def initWidget(self):
		''' '''
		self.buildPane()
		return self
	def buildPane(self):
		''' '''
		layout = pyqt.QVBoxLayout()
		wdgt = annotations.NchantdLabel(self.config.dikt['label']['text'])
		layout.setAlignment(wdgt, pyqt.Qt.AlignTop)
		layout.addWidget(wdgt)
		wdgt = NchantdComboBox(self)
		layout.setAlignment(wdgt, pyqt.Qt.AlignTop)
		layout.addWidget(wdgt)
		self.setLayout(layout)
		return self


class NchantdEqualButton():
	''' '''
	def __init__(self):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)


class NchantdFxButton():
	'''Apply given function (addition, subtraction, etc) to current mathematical
		equation'''
	def __init__(self):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)


class NchantdIncrementbox(pyqt.QSpinBox):
	''' '''
	def __init__(self, cfg, parent=None):
		'''https://www.tutorialspoint.com/pyqt/pyqt_qspinbox_self.htm'''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdIncrementbox, self).__init__(cfg['name'], parent)
		self.setMinimum(cfg['min'])
		self.setMaximum(cfg['max'])
		self.setRange(cfg['range'])
		self.setValue(cfg['default_value'])
		self.valueChanged.connect(getattr(app, cfg['handlers']['value_changed_handler']))


class NchantdMathPad(pyqt.QWidget):
	''' '''
	def __init__(self):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)


class NchantdNumberButton():
	''' '''
	def __init__(self):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)


class NchantdNumberPad(pyqt.QWidget):
	''' '''
	def __init__(self, parent=None, cfg=None):
		''' '''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		self.parent = parent
		pyqt.QWidget.__init__(self)
		self.initUI()
	def initUI(self):
		''' '''
		self.layout = pyqt.QGridLayout()
		self.btn_one = pyqt.NchantdButton('1').initWidget()
		self.layout.addWidget(self.btn_one, 0, 0, 0, 0)
		self.btn_two = pyqt.NchantdButton('2').initWidget()
		self.layout.addWidget(self.btn_two, 0, 0, 0, 0)
		self.btn_three = pyqt.NchantdButton('3').initWidget()
		self.layout.addWidget(self.btn_three, 0, 0, 0, 0)
		self.btn_four = pyqt.NchantdButton('4').initWidget()
		self.layout.addWidget(self.btn_four, 0, 0, 0, 0)
		self.btn_five = pyqt.NchantdButton('5').initWidget()
		self.layout.addWidget(self.btn_five, 0, 0, 0, 0)
		self.btn_six = pyqt.NchantdButton('6').initWidget()
		self.layout.addWidget(self.btn_six, 0, 0, 0, 0)
		self.btn_seven = pyqt.NchantdButton('7').initWidget()
		self.layout.addWidget(self.btn_seven, 0, 0, 0, 0)
		self.btn_eight = pyqt.NchantdButton('8').initWidget()
		self.layout.addWidget(self.btn_eight, 0, 0, 0, 0)
		self.btn_nine = pyqt.NchantdButton('9').initWidget()
		self.layout.addWidget(self.btn_nine, 0, 0, 0, 0)
		self.btn_zero = pyqt.NchantdButton('0').initWidget()
		self.layout.addWidget(self.btn_zero, 0, 0, 0, 0)
		self.btn_plus = pyqt.NchantdButton('+').initWidget()
		self.layout.addWidget(self.btn_plus, 0, 0, 0, 0)
		self.btn_minus = pyqt.NchantdButton('-').initWidget()
		self.layout.addWidget(self.btn_minus, 0, 0, 0, 0)
		self.btn_equal = pyqt.NchantdButton('=').initWidget()
		self.layout.addWidget(self.btn_equal, 0, 0, 0, 0)
		self.btn_multiply = pyqt.NchantdButton('*').initWidget()
		self.layout.addWidget(self.btn_multiply, 0, 0, 0, 0)
		self.btn_divide = pyqt.NchantdButton('/').initWidget()
		self.layout.addWidget(self.btn_divide, 0, 0, 0, 0)
		self.btn_decimal = pyqt.NchantdButton('.').initWidget()
		self.layout.addWidget(self.btn_decimal, 0, 0, 0, 0)
		self.config.dikt['buttons']['zero']['text'] = '0'
		self.newbutton= NchantdButton(self, self.config.dikt['buttons']['new'])
		self.layout.addWidget(self.newbutton)
		self.setLayout(self.layout)


class NchantdRadioButton(pyqt.QRadioButton):
	def __init__(self, cfg, parent=None):
		''' https://www.tutorialspoint.com/pyqt/pyqt_qradiobutton_self.htm'''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdRadioButton, self).__init__(cfg['name'], parent)
		self.setChecked(cfg['checked'])
		self.setText(cfg['label'])
		self.toggled.connect(getattr(app, cfg['handlers']['toggled_handler']))


class NchantdSliderButton(pyqt.QSlider):
	''' '''
	def __init__(self, cfg, parent=None):
		'''	https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm'''
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(QSlider, self).__init__(cfg['name'])
		self.setMinimum(cfg['min'])
		self.setMaximum(cfg['max'])
		self.setSingleStep(cfg['step'])
		self.setValue(cfg['default_value'])
		self.setTickInterval(cfg['tickinterval'])
		self.setTickPosition(cfg['tickposition'])
		self.valueChanged.connect(getattr(app, cfg['handlers']['value_changed_handler']))
		self.sliderPressed.connect(getattr(app, cfg['handlers']['slider_pressed_handler']))
		self.sliderMoved.connect(getattr(app, cfg['handlers']['slider_moved_handler']))
		self.sliderReleased.connect(getattr(app, cfg['handlers']['slider_released_handler']))


class NchantdSubmissionButtons(pyqt.QWidget):
	'''A single pane widget with a button set for submitting a form '''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.config = condor.instruct(pxcfg).override(cfg)
		self.config.select('NchantdSubmissionButtons')
		if parent:
			self.config.override(parent.config)
		self.parent = parent
		pyqt.QWidget.__init__(self)
		self.layout = pyqt.QHBoxLayout()
		if log: print('Nchantd Submission Buttons', self.config.dikt)
		self.config.dikt['buttons']['new']['text'] = 'New'
		self.newbutton = NchantdButton(self, self.config.dikt['buttons']['new'])
		self.newbutton.initWidget()
		self.layout.addWidget(self.newbutton)
		self.config.dikt['buttons']['submit']['text'] = 'Submit'
		self.submitbutton = NchantdButton(self, self.config.dikt['buttons']['submit'])
		self.submitbutton.initWidget()
		self.layout.addWidget(self.submitbutton)
		self.config.dikt['buttons']['delete']['text'] = 'Delete'
		self.deletebutton = NchantdButton(self, self.config.dikt['buttons']['delete'])
		self.deletebutton.initWidget()
		self.layout.addWidget(self.deletebutton)
		self.setLayout(self.layout)
	def initWidget(self):
		''' '''
		return self


class NchantdToggleButton(NchantdButton):
	'''A widget providing an on/off control via a checkable button'''
	def __init__(self, parent=None, cfg={}):
		''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdToggleButton')
		if parent:
			self.config.override(parent.config)
		self.config.dikt['checkable'] = True
		super(NchantdToggleButton, self).__init__(parent)
		self.config.override(cfg)


class NchantdToolButton(pyqt.QToolButton):
	''' '''
	def __init__(self):
		if parent:
			cfg = parent.config
		self.config = condor.instruct(pxcfg).override(cfg)
		super(NchantdToolButton, self).__init__(self)


class NchantdMenu():
	''' '''
	def __init__(self):
		''' '''
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self


class NcantdMenuBar():
	''' '''
	def __init__(self):
		''' '''
	def initModel(self):
		''' '''
		return self
	def initView(self):
		''' '''
		return self
	def initWidget(self):
		''' '''
		return self


#===========================Code Source Examples================================||
'''
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
