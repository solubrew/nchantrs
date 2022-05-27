

class character(who):

class bots:

class maps:

class equipment:



class who(thing):
	def __init__(self, display):
		thing.__init__(display)

class what(thing):
	def __init__(self, display):
		thing.__init__(display)

class where(thing):
	def __init__(self, display):
		thing.__init__(display)

class when(thing):
	def __init__(self, display):
		thing.__init__(display)


class thing:
	''
	def __init__(self, name, display, cfg=None):
		if cfg != None:
			self.config = config.instruct(loci).select(self.thing).dikt
		self.name = name
		self.display = display
	def write(self, x, y):
		''
		self.display.blit(ballImg, (x,y))
	def boundary(self):
		''
		self.shape():
		self.rarea = [[x0,y0], [x1,y1], [x2,y2], [x3,y3]]
		self.fullmap =
		return self
	def loadConfig(self, loci):
		''
		self.thing = config.instruct(loci).select(self.name).dikt
		return self
	def loadData(self):
		''
		self.imgs = self.thing['imgs']
		self.thgimg = pygame.image.load(self.imgs['0'])
		return self
	def createSheet(self, x, y, n):
		'Create a sheet of size x by y with n spaces'
		return self
	def mapSheet(self):
		'Map iterations to each space on the sheet'
		return self





