#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Nchantrs@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''	#																			||
---	#																			||
<(META)>:	#																	||
	docid: ''	#							||
	name: Python Document#								||
	description: >	#															||
	expirary: <[expiration]>	#													||
	version: <[version]>	#														||
	path: <[LEXIvrs]>	#														||
	outline: <[outline]>	#														||
	authority: document|this	#													||
	security: sec|lvl2	#														||
	<(WT)>: -32	#																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#================================Core Modules===================================||
from os.path import abspath, dirname, exists, join
import glob, math
from collections import namedtuple
#===============================================================================||
from condor import condor

from nchantrs.libraries import pyqt
from nchantrs.models.tablemodels import NchantdTableModel
from nchantrs.views.tableviews import NchantdTableView
#===============================================================================||

#===============================================================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = True
#===============================================================================||
pxcfg = f'{here}/_data_/viewers.yaml'

preview = namedtuple("preview", "id title image")

NUMBER_OF_COLUMNS = 4
CELL_PADDING = 20 # all sides

class NchantdThumbnailViewerPane(pyqt.QWidget):
	''' '''
	def __init__(self, parent=None, cfg={}):
		'''' '''
		self.parent = parent
		self.config = condor.instruct(pxcfg).select('NchantdThumbnailViewerPane')
		self.config.override(cfg)
		super(NchantdThumbnailViewerPane, self).__init__()
		#self.view = NchantdTableView(parent, self.config)

		self.view = pyqt.QTableView()
		self.view.horizontalHeader().hide()
		self.view.verticalHeader().hide()
		self.view.setGridStyle(pyqt.Qt.NoPen)

		delegate = PreviewDelegate()
		self.view.setItemDelegate(delegate)
		self.model = PreviewModel()
		self.view.setModel(self.model)

#		self.setCentralWidget(self.view)

		#self.model = NchantdTableModel(parent, self.config)
		self.model = PreviewModel()


	def initModel(self):
		''' '''
		return self

	def initView(self):
		''' '''
		return self

	def initWidget(self):
		''' '''

		self.loadImages()
		return self

	def loadImages(self, path=None):
		''' '''
		images = ['*.jpg', '*.png', '*.jpeg']
		path = '/home/solubrew/OPs/3_Work/opENGRg/3_Work/jobPhanessaSys/AIGen'
		for n, fn in enumerate(glob.glob(f'{path}/*.jpg')):

			image = pyqt.QImage(fn)
			item = preview(n, fn, image)
			self.model.previews.append(item)
		self.model.layoutChanged.emit()

class PreviewDelegate(pyqt.QStyledItemDelegate):

		def paint(self, painter, option, index):
				# data is our preview object
				data = index.model().data(index, Qt.DisplayRole)
				if data is None:
						return

				width = option.rect.width() - CELL_PADDING * 2
				height = option.rect.height() - CELL_PADDING * 2

				# option.rect holds the area we are painting on the widget (our table cell)
				# scale our pixmap to fit
				scaled = data.image.scaled(
						width,
						height,
						aspectRatioMode=Qt.KeepAspectRatio,
				)
				# Position in the middle of the area.
				x = CELL_PADDING + (width - scaled.width()) / 2
				y = CELL_PADDING + (height - scaled.height()) / 2

				painter.drawImage(option.rect.x() + x, option.rect.y() + y, scaled)

		def sizeHint(self, option, index):
				# All items the same size.
				return QSize(300, 200)
class PreviewModel(pyqt.QAbstractTableModel):
		def __init__(self, todos=None):
				super().__init__()
				# .data holds our data for display, as a list of Preview objects.
				self.previews = []

		def data(self, index, role):
				try:
						data = self.previews[index.row() * 4 + index.column() ]
				except IndexError:
						# Incomplete last row.
						return

				if role == Qt.DisplayRole:
						return data	 # Pass the data to our delegate to draw.

				if role == Qt.ToolTipRole:
						return data.title

		def columnCount(self, index):
				return NUMBER_OF_COLUMNS

		def rowCount(self, index):
				n_items = len(self.previews)
				return math.ceil(n_items / NUMBER_OF_COLUMNS)
