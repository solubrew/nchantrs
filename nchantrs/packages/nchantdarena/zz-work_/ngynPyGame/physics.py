
class threeD:
	version='0.0.0.0.0.0'
	def __init__(self, cfg=None):

class twoD:
	''
	version='0.0.0.0.0.0'
	def __init__(self, cfg=None):
		self.scale(**cfg['scale'])
		self.drag(**cfg['drag'])
	def drag(self, viscos):
		self.ratemod = viscos
	def gravity(self, ncycles, view='sideroller'):
		'Gravity Acceleration at Scale'
		gforce_magnitude = ncycles*self.gravrt
		if view == 'sideroller':
			gforce_vector = '+y'
		if view == 'topdown':
			gforce_vector = '-z':
		self.gforce = [gforce_magnitude, gforce_vector]
		return self
	def scale(self, ppm=4, cps=60, g=9.8, mod=1):
		'Scale the World in Meters to Pixels for the Given World'
		if mod < 1:
			mod0 = 1-mod
		else:
			mod0 = mod
		self.xm, self.zm = ppm*mod0, ppm*mod#pixels per meter
		self.cps = cps#cycles per second
		self.gravrt = g#					meters per second
		return self
	def trajectories(self):
		''
		return self





