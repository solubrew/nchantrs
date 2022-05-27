
"""
Orange canvas about dialog
"""
import sys
import pkg_resources
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
import config
ABOUT_TEMPLATE = """\
<center>
<h4>Orange</h4>
<p>Version: {version}</p>
<p>(git revision: {git_revision})</p>
</center>
"""
class AboutDialog(QDialog):
	def __init__(self, parent=None, **kwargs):
		QDialog.__init__(self, parent, **kwargs)
		if sys.platform == "darwin":
			self.setAttribute(Qt.WA_MacSmallSize, True)
		self.__setupUi()
	def __setupUi(self):
		layout = QVBoxLayout()
		label = QLabel(self)
		pixmap, _ = config.splash_screen()
		label.setPixmap(pixmap)
		layout.addWidget(label, Qt.AlignCenter)
		try:
			from Orange.version import version
			from Orange.version import git_revision
		except ImportError:
			dist = pkg_resources.get_distribution("Orange3")
			version = dist.version
			git_revision = "Unknown"
		text = ABOUT_TEMPLATE.format(version=version,
									 git_revision=git_revision[:7])
		# TODO: Also list all known add-on versions.
		text_label = QLabel(text)
		layout.addWidget(text_label, Qt.AlignCenter)
		buttons = QDialogButtonBox(QDialogButtonBox.Close,
								   Qt.Horizontal,
								   self)
		layout.addWidget(buttons)
		buttons.rejected.connect(self.accept)
		layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
		self.setLayout(layout)
	def about(self):
		link = "<p><a title='Axel Schneider' href='http://goodoldsongs.jimdo.com' target='_blank'>Axel Schneider</a></p>"
		title = "über QTextEdit"
		message =  ("<span style='text-shadow: #2e3436 2px 2px 2px; color: #6169e1; font-size: 24pt;font-weight: bold;'><strong>QTextEdit 1.2</strong></span></p><br><br>created by<h2 >" + link + "</h2> with PyQt5"
					"<br><br>Copyright © 2018 The Qt Company Ltd and other contributors."
					"<br>Qt and the Qt logo are trademarks of The Qt Company Ltd.")
		msg = QMessageBox(QMessageBox.Information, title, message, QMessageBox.NoButton, self, Qt.Dialog|Qt.NoDropShadowWindowHint).show()
	# ask for anonymous data collection permission
	def requestDataCollectionPermission():
		permDialogButtons = MessageOverlayWidget.AcceptRole | MessageOverlayWidget.RejectRole
		permDialog = MessageOverlayWidget(parent=w,
										  text="Do you wish to share anonymous usage "
											   "statistics to help improve Orange?",
										  wordWrap=True,
										  standardButtons=permDialogButtons)
		btnOK = permDialog.button(MessageOverlayWidget.AcceptRole)
		btnOK.setText("Allow")
		def respondToRequest():
			settings["error-reporting/permission-requested"] = True
		def shareData():
			settings["error-reporting/send-statistics"] = True
		permDialog.clicked.connect(respondToRequest)
		permDialog.accepted.connect(shareData)
		permDialog.setStyleSheet("""MessageOverlayWidget {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop:0 #666, stop:0.3 #6D6D6D, stop:1 #666)}
									MessageOverlayWidget QLabel#text-label {color: white;}""")
		permDialog.setWidget(w)
		permDialog.show()
	settings = config.settings()
	if not settings["error-reporting/permission-requested"]:
		requestDataCollectionPermission()
