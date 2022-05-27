

from nchantrs.dialogs import dialogs

class Preferences(dialogs.Sigil):
	''' '''
	def __init__(self, app, cfg: dict={}, parent=None):
		''' '''
		super(Preferences, self).__init__(parent)
		mainLayout = pyqt.QVBoxLayout()

		preferencesGB = pyqt.QGroupBox()
		preferencesLayout = pyqt.QGridLayout()
		if 'wdigets' in cfg.keys():
			for widget in cfg['widgets']:
				preferencesLayout.addWidget(widget)
		preferencesGB.setLayout(preferencesLayout)
		preferencesGB.setFixedHeight(400)
		mainLayout.addWidget(preferencesGB)

		buttonsGB = pyqt.QGroupBox()
		buttonsLayout = pyqt.QHBoxLayout()
		self.createSaveButton()
		buttonsLayout.addWidget(self.btn_save)
		self.createCloseButton()
		buttonsLayout.addWidget(self.btn_close)
		buttonsGB.setLayout(buttonsLayout)
		buttonsGB.setFixedHeight(80)
		mainLayout.addWidget(buttonsGB)
		mainLayout.setAlignment(buttonsGB, pyqt.Qt.AlignBottom)

		self.setLayout(mainLayout)
		self.setStyleSheet(open(qss, "r").read())#								||
		self.setGeometry(pyqt.QRect(500, 200, 800, 500))
		self.setWindowTitle('Preferences')
		self.exec_()
	def createSaveButton(self):
		''' '''
		self.btn_save = Button('Save')
		return self
	def createCloseButton(self):
		''' '''
		self.btn_close = Button('Close')
		return self
