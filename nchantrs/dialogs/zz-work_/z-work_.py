




#########################################
from PyQt5.QtCore import QEvent, QRectF, Qt, QTimeLine
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPixmap,
        QTransform)
from PyQt5.QtWidgets import (QApplication, QDialog, QGraphicsItem,
        QGraphicsProxyWidget, QGraphicsScene, QGraphicsView, QStyleFactory,
        QWidget)
import embeddeddialogs_rc
from embeddeddialog import Ui_embeddedDialog
class CustomProxy(QGraphicsProxyWidget):
    def __init__(self, parent=None, wFlags=0):
        super(CustomProxy, self).__init__(parent, wFlags)
        self.popupShown = False
        self.currentPopup = None
        self.timeLine = QTimeLine(250, self)
        self.timeLine.valueChanged.connect(self.updateStep)
        self.timeLine.stateChanged.connect(self.stateChanged)
    def boundingRect(self):
        return QGraphicsProxyWidget.boundingRect(self).adjusted(0, 0, 10, 10)
    def paintWindowFrame(self, painter, option, widget):
        color = QColor(0, 0, 0, 64)
        r = self.windowFrameRect()
        right = QRectF(r.right(), r.top()+10, 10, r.height()-10)
        bottom = QRectF(r.left()+10, r.bottom(), r.width(), 10)
        intersectsRight = right.intersects(option.exposedRect)
        intersectsBottom = bottom.intersects(option.exposedRect)
        if intersectsRight and intersectsBottom:
            path = QPainterPath()
            path.addRect(right)
            path.addRect(bottom)
            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)
        elif intersectsBottom:
            painter.fillRect(bottom, color)
        elif intersectsRight:
            painter.fillRect(right, color)
        super(CustomProxy, self).paintWindowFrame(painter, option, widget)
    def hoverEnterEvent(self, event):
        super(CustomProxy, self).hoverEnterEvent(event)
        self.scene().setActiveWindow(self)
        if self.timeLine.currentValue != 1:
            self.zoomIn()
    def hoverLeaveEvent(self, event):
        super(CustomProxy, self).hoverLeaveEvent(event)
        if not self.popupShown and (self.timeLine.direction() != QTimeLine.Backward or self.timeLine.currentValue() != 0):
            self.zoomOut()
    def sceneEventFilter(self, watched, event):
        if watched.isWindow() and (event.type() == QEvent.UngrabMouse or event.type() == QEvent.GrabMouse):
            self.popupShown = watched.isVisible()
            if not self.popupShown and not self.isUnderMouse():
                self.zoomOut()
        return super(CustomProxy, self).sceneEventFilter(watched, event)
    def itemChange(self, change, value):
        if change == self.ItemChildAddedChange or change == self.ItemChildRemovedChange :
            if change == self.ItemChildAddedChange:
                self.currentPopup = value
                self.currentPopup.setCacheMode(self.ItemCoordinateCache)
                if self.scene() is not None:
                    self.currentPopup.installSceneEventFilter(self)
            elif self.scene() is not None:
                self.currentPopup.removeSceneEventFilter(self)
                self.currentPopup = None
        elif self.currentPopup is not None and change == self.ItemSceneHasChanged:
                self.currentPopup.installSceneEventFilter(self)
        return super(CustomProxy, self).itemChange(change, value)
    def updateStep(self, step):
        r = self.boundingRect()
        self.setTransform(QTransform() \
                            .translate(r.width() / 2, r.height() / 2)\
                            .rotate(step * 30, Qt.XAxis)\
                            .rotate(step * 10, Qt.YAxis)\
                            .rotate(step * 5, Qt.ZAxis)\
                            .scale(1 + 1.5 * step, 1 + 1.5 * step)\
                            .translate(-r.width() / 2, -r.height() / 2))
    def stateChanged(self, state):
        if state == QTimeLine.Running:
            if self.timeLine.direction() == QTimeLine.Forward:
                self.setCacheMode(self.NoCache)
        elif state == QTimeLine.NotRunning:
            if self.timeLine.direction() == QTimeLine.Backward:
                self.setCacheMode(self.DeviceCoordinateCache)
    def zoomIn(self):
        if self.timeLine.direction() != QTimeLine.Forward:
            self.timeLine.setDirection(QTimeLine.Forward)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()
    def zoomOut(self):
        if self.timeLine.direction() != QTimeLine.Backward:
            self.timeLine.setDirection(QTimeLine.Backward)
        if self.timeLine.state() == QTimeLine.NotRunning:
            self.timeLine.start()
class EmbeddedDialog(QDialog):
    def __init__(self, parent=None):
        super(EmbeddedDialog, self).__init__(parent)
        self.ui = Ui_embeddedDialog()
        self.ui.setupUi(self)
        self.ui.layoutDirection.setCurrentIndex(self.layoutDirection() != Qt.LeftToRight)
        for styleName in QStyleFactory.keys():
            self.ui.style.addItem(styleName)
            if self.style().objectName().lower() == styleName.lower():
                self.ui.style.setCurrentIndex(self.ui.style.count() -1)
        self.ui.layoutDirection.activated.connect(self.layoutDirectionChanged)
        self.ui.spacing.valueChanged.connect(self.spacingChanged)
        self.ui.fontComboBox.currentFontChanged.connect(self.fontChanged)
        self.ui.style.activated[str].connect(self.styleChanged)
    def layoutDirectionChanged(self, index):
        if index == 0:
            self.setLayoutDirection(Qt.LeftToRight)
        else:
            self.setLayoutDirection(Qt.RightToLeft)
    def spacingChanged(self, spacing):
        self.layout().setSpacing(spacing)
        self.adjustSize()
    def fontChanged(self, font):
        self.setFont(font)
    def setStyleHelper(self, widget, style):
        widget.setStyle(style)
        widget.setPalette(style.standardPalette())
        for child in widget.children():
            if isinstance(child, QWidget):
                self.setStyleHelper(child, style)
    def styleChanged(self, styleName):
        style = QStyleFactory.create(styleName)
        if style:
            self.setStyleHelper(self, style)
        # Keep a reference to the style.
        self._style = style
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    scene.setStickyFocus(True)
    for y in range(10):
        for x in range(10):
            proxy = CustomProxy(None, Qt.Window)
            proxy.setWidget(EmbeddedDialog())
            rect = proxy.boundingRect()
            proxy.setPos( x * rect.width()*1.05, y*rect.height()*1.05 )
            proxy.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
            scene.addItem(proxy)
    scene.setSceneRect(scene.itemsBoundingRect())
    view = QGraphicsView(scene)
    view.scale(0.5, 0.5)
    view.setRenderHints(view.renderHints() | QPainter.Antialiasing  | QPainter.SmoothPixmapTransform)
    view.setBackgroundBrush(QBrush(QPixmap(':/No-Ones-Laughing-3.jpg')))
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
    view.show()
    view.setWindowTitle("Embedded Dialogs Demo")
    sys.exit(app.exec_())




from PyQt5 import QtCore, QtGui, QtWidgets
class Ui_embeddedDialog(object):
	def setupUi(self, embeddedDialog):
		embeddedDialog.setObjectName("embeddedDialog")
		embeddedDialog.resize(407, 134)
		self.formLayout = QtWidgets.QFormLayout(embeddedDialog)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(embeddedDialog)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.layoutDirection = QtWidgets.QComboBox(embeddedDialog)
		self.layoutDirection.setObjectName("layoutDirection")
		self.layoutDirection.addItem("")
		self.layoutDirection.addItem("")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.layoutDirection)
		self.label_2 = QtWidgets.QLabel(embeddedDialog)
		self.label_2.setObjectName("label_2")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
		self.fontComboBox = QtWidgets.QFontComboBox(embeddedDialog)
		self.fontComboBox.setObjectName("fontComboBox")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.fontComboBox)
		self.label_3 = QtWidgets.QLabel(embeddedDialog)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
		self.style = QtWidgets.QComboBox(embeddedDialog)
		self.style.setObjectName("style")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.style)
		self.label_4 = QtWidgets.QLabel(embeddedDialog)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.spacing = QtWidgets.QSlider(embeddedDialog)
		self.spacing.setOrientation(QtCore.Qt.Horizontal)
		self.spacing.setObjectName("spacing")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spacing)
		self.label.setBuddy(self.layoutDirection)
		self.label_2.setBuddy(self.fontComboBox)
		self.label_3.setBuddy(self.style)
		self.label_4.setBuddy(self.spacing)
		self.retranslateUi(embeddedDialog)
		QtCore.QMetaObject.connectSlotsByName(embeddedDialog)
	def retranslateUi(self, embeddedDialog):
		_translate = QtCore.QCoreApplication.translate
		embeddedDialog.setWindowTitle(_translate("embeddedDialog", "Embedded Dialog"))
		self.label.setText(_translate("embeddedDialog", "Layout Direction:"))
		self.layoutDirection.setItemText(0, _translate("embeddedDialog", "Left to Right"))
		self.layoutDirection.setItemText(1, _translate("embeddedDialog", "Right to Left"))
		self.label_2.setText(_translate("embeddedDialog", "Select Font:"))
		self.label_3.setText(_translate("embeddedDialog", "Style:"))
		self.label_4.setText(_translate("embeddedDialog", "Layout spacing:"))
#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##	 notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##	 notice, this list of conditions and the following disclaimer in
##	 the documentation and/or other materials provided with the
##	 distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##	 the names of its contributors may be used to endorse or promote
##	 products derived from this software without specific prior written
##	 permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
		QDialogButtonBox, QFrame, QGroupBox, QLabel, QLineEdit, QListWidget,
		QTabWidget, QVBoxLayout, QWidget)
class TabDialog(QDialog):
	def __init__(self, fileName, parent=None):
		super(TabDialog, self).__init__(parent)
		fileInfo = QFileInfo(fileName)
		tabWidget = QTabWidget()
		tabWidget.addTab(GeneralTab(fileInfo), "General")
		tabWidget.addTab(PermissionsTab(fileInfo), "Permissions")
		tabWidget.addTab(ApplicationsTab(fileInfo), "Applications")
		buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(tabWidget)
		mainLayout.addWidget(buttonBox)
		self.setLayout(mainLayout)
		self.setWindowTitle("Tab Dialog")
class GeneralTab(QWidget):
	def __init__(self, fileInfo, parent=None):
		super(GeneralTab, self).__init__(parent)
		fileNameLabel = QLabel("File Name:")
		fileNameEdit = QLineEdit(fileInfo.fileName())
		pathLabel = QLabel("Path:")
		pathValueLabel = QLabel(fileInfo.absoluteFilePath())
		pathValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		sizeLabel = QLabel("Size:")
		size = fileInfo.size() // 1024
		sizeValueLabel = QLabel("%d K" % size)
		sizeValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		lastReadLabel = QLabel("Last Read:")
		lastReadValueLabel = QLabel(fileInfo.lastRead().toString())
		lastReadValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		lastModLabel = QLabel("Last Modified:")
		lastModValueLabel = QLabel(fileInfo.lastModified().toString())
		lastModValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(fileNameLabel)
		mainLayout.addWidget(fileNameEdit)
		mainLayout.addWidget(pathLabel)
		mainLayout.addWidget(pathValueLabel)
		mainLayout.addWidget(sizeLabel)
		mainLayout.addWidget(sizeValueLabel)
		mainLayout.addWidget(lastReadLabel)
		mainLayout.addWidget(lastReadValueLabel)
		mainLayout.addWidget(lastModLabel)
		mainLayout.addWidget(lastModValueLabel)
		mainLayout.addStretch(1)
		self.setLayout(mainLayout)
class PermissionsTab(QWidget):
	def __init__(self, fileInfo, parent=None):
		super(PermissionsTab, self).__init__(parent)
		permissionsGroup = QGroupBox("Permissions")
		readable = QCheckBox("Readable")
		if fileInfo.isReadable():
			readable.setChecked(True)
		writable = QCheckBox("Writable")
		if fileInfo.isWritable():
			writable.setChecked(True)
		executable = QCheckBox("Executable")
		if fileInfo.isExecutable():
			executable.setChecked(True)
		ownerGroup = QGroupBox("Ownership")
		ownerLabel = QLabel("Owner")
		ownerValueLabel = QLabel(fileInfo.owner())
		ownerValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		groupLabel = QLabel("Group")
		groupValueLabel = QLabel(fileInfo.group())
		groupValueLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
		permissionsLayout = QVBoxLayout()
		permissionsLayout.addWidget(readable)
		permissionsLayout.addWidget(writable)
		permissionsLayout.addWidget(executable)
		permissionsGroup.setLayout(permissionsLayout)
		ownerLayout = QVBoxLayout()
		ownerLayout.addWidget(ownerLabel)
		ownerLayout.addWidget(ownerValueLabel)
		ownerLayout.addWidget(groupLabel)
		ownerLayout.addWidget(groupValueLabel)
		ownerGroup.setLayout(ownerLayout)
		mainLayout = QVBoxLayout()
		mainLayout.addWidget(permissionsGroup)
		mainLayout.addWidget(ownerGroup)
		mainLayout.addStretch(1)
		self.setLayout(mainLayout)
class ApplicationsTab(QWidget):
	def __init__(self, fileInfo, parent=None):
		super(ApplicationsTab, self).__init__(parent)
		topLabel = QLabel("Open with:")
		applicationsListBox = QListWidget()
		applications = []
		for i in range(1, 31):
			applications.append("Application %d" % i)
		applicationsListBox.insertItems(0, applications)
		alwaysCheckBox = QCheckBox()
		if fileInfo.suffix():
			alwaysCheckBox = QCheckBox("Always use this application to open "
					"files with the extension '%s'" % fileInfo.suffix())
		else:
			alwaysCheckBox = QCheckBox("Always use this application to open "
					"this type of file")
		layout = QVBoxLayout()
		layout.addWidget(topLabel)
		layout.addWidget(applicationsListBox)
		layout.addWidget(alwaysCheckBox)
		self.setLayout(layout)
if __name__ == '__main__':
	import sys
	app = QApplication(sys.argv)
	if len(sys.argv) >= 2:
		fileName = sys.argv[1]
	else:
		fileName = "."
	tabdialog = TabDialog(fileName)
	tabdialog.show()
	sys.exit(app.exec_())
