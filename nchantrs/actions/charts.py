#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: <^(UUID)^>
	name:
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
import logging

logger = logging.getLogger(__name__)


def addchart() -> None:
	'''Open a dialog to create a new sheet and place a chart widget.  The dialog
	allows for data selection and chart type with the ability to point to a
	config file or select a style for the chart that will get used into the
	pyffice document.  Selecting of a config file will give the option to create
	a style from it at that point'''
	logger.debug("addchart called")
	return
def editchart() -> None:
	'''Open dialog to edit selected chart'''
	logger.debug("editchart called")
	return
def plotarea() -> None:
	'''Plot Area Chart '''
	logger.debug("plotarea called")
	return
def plotbar() -> None:
	'Plot Bar Chart'
	logger.debug("plotbar called")
	return
def plotbubble() -> None:
	'Plot Bubble Chart'
	logger.debug("plotbubble called")
	return
def plotfittedline() -> None:
	'Plot Fitted Line Chart'
	logger.debug("plotfittedline called")
	return
def plotline() -> None:
	'Plot Line Chart'
	logger.debug("plotline called")
	return
def plotpie() -> None:
	'Plot Pie Chart'
	logger.debug("plotpie called")
	return
def plotscatter() -> None:
	'Plot Scatter Chart'
	logger.debug("plotscatter called")
	return
def plottimeseries() -> None:
	'Plot Time Series Chart'
	logger.debug("plottimeseries called")
	return
