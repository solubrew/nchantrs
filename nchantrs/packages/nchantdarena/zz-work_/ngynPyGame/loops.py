'''
---
<(META)>:
	DOCid: <^[uuid]^>
	name: Ecosystems Level Module Initation Document
	description: >

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>/panda/LEXI/tmplts/tmpltPANDA/<(meta)>/metadoc.yaml
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
import pygame, time, random

class linear_classic:
	def __init__(self, cfg=None):
		pygame.init()
		self.confg = config.instruct(pxcfg).select('loop').override(cfg)
		x = self.config['screen']['size']['x']
		y = self.config['screen']['size']['y']
		screen_name = self.config['screeen']['name']
		self.display = pygame.display.set_mode((x,y))# create window
		pygame.display.set_caption(screen_name)
		self.clock = pygame.time.Clock()
	def clean(self):
		'remove all expired items from the screen'
		return self
	def ctrlr(self, vnt):
		controls.keyboard(vnt)
		return self
	def detect(self):
		'detect any object interactions'
		collions.entangle(self.objs)
		return self
	def paint(self):
		''
		return self
	def decal(self):
		''
		self.objs = sprites.update()
		self.detect(self.objs)
		return self
	def quit(self):
		pygame.quit()
		quit()
	def run(self):
		stop = False
		while not stop:
			for event in pygame.event.get():#gets all events
				self.control(event)
			self.paint()
			self.decal()
		pygame.display.update()
		clock.tick(60)

class linear_forked:
	'Handle Turned Based and complex action initation within a blocking loop'
	def __init__(self, cfg=None):

	def setPlayers(self):

	def

class parallel_controlled:
	def __init__(self, cfg=None):
class parallel_ai
	def __init__(self, cfg=None):

