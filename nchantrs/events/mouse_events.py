
class mouseCTRLR():
	def __init__():
	def mousePressEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.mousePressEvent(event):
			return
		# Right (context) click on the node item. If the widget is not
		# in the current selection then select the widget (only the widget).
		# Else simply return and let customContextMenuRequested signal
		# handle it
		shape_item = self.item_at(event.scenePos(), items.NodeItem)
		if shape_item and event.button() == Qt.RightButton and shape_item.flags() & QGraphicsItem.ItemIsSelectable:
			if not shape_item.isSelected():
				self.clearSelection()
				shape_item.setSelected(True)
		return QGraphicsScene.mousePressEvent(self, event)
	def mouseMoveEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.mouseMoveEvent(event):
			return
		return QGraphicsScene.mouseMoveEvent(self, event)
	def mouseReleaseEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.mouseReleaseEvent(event):
			return
		return QGraphicsScene.mouseReleaseEvent(self, event)
	def mouseDoubleClickEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.mouseDoubleClickEvent(event):
			return
		return QGraphicsScene.mouseDoubleClickEvent(self, event)
	def keyPressEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.keyPressEvent(event):
			return
		return QGraphicsScene.keyPressEvent(self, event)
	def keyReleaseEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.keyReleaseEvent(event):
			return
		return QGraphicsScene.keyReleaseEvent(self, event)
	def contextMenuEvent(self, event):
		if self.user_interaction_handler and self.user_interaction_handler.contextMenuEvent(event):
			return
		super().contextMenuEvent(event)
	def set_user_interaction_handler(self, handler):
		if self.user_interaction_handler and not self.user_interaction_handler.isFinished():
			self.user_interaction_handler.cancel()
#		log.info("Setting interaction '%s' to '%s'" % (handler, self))
		self.user_interaction_handler = handler
		if handler:
			handler.start()
	def __str__(self):
		return "%s(objectName=%r, ...)" % \
				(type(self).__name__, str(self.objectName()))
def on_clickleft_press(widget, event):
	'''Action to take upon event of mouse left click press'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
		super().mousePressEvent(event)
		widget.setFocus()
	return
def on_clickleft_release():
	'''Action to take upon event of mouse left click release'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_clickleftdouble():
	'''Action to take upon event of mouse double left click'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_clickmiddle_press():
	'''Action to take upon event of mouse middle click'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_clickmiddle_release():
	'''Action to take upon event of mouse middle click'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  pass
	return
def on_clickright_press():
	'''Action to take upon event of mouse right click press'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  action.context_menu()
	return
def on_clickright_release():
	'''Action to take upon event of mouse right click release'''
	if ctrl == True:
		pass
	elif shift == True:
		pass
	elif alt == True:
		pass
	else:
	  action.context_menu()
	return
def on_wheel_forward():
	''' '''
def on_wheel_backward():
	''' '''
