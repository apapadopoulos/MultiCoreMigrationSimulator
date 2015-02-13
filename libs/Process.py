import numpy as np
import scipy as sp

class Process:
	"""Process description. It is implementing the
	   y(k+1) = u(k) + d(k)
	   where
	   - y(k) is the time that the process spent on the CPU
	   - u(k) is the time that the process is supposed to spend on the CPU
	   - d(k) is a disturbance related to critical sections/blocking
	   The disturbance is here modeled as a random quantity with gaussian
	   distribution and bounded variance.

	"""
	def __init__(self, ident, alpha=1, y0=0, stdDev=0.01):
		self.id     = ident
		self.stdDev = stdDev
		self.y      = y0
		self.alpha  = alpha    # desired percentage of utilization

	def getY(self):
		return self.y

	def setU(self, u):
		self.y = max(u + np.random.randn()*self.stdDev,0);

	def viewProcess(self):
		print '[Process%d] alpha=%g,\tstdDev = %g,\t y0=%g'%\
		         (self.id,self.alpha,self.stdDev,self.y)

	def getName(self):
		return 'Process'+str(self.id)

	def getID(self):
		return self.id

	def getAlpha(self):
		return self.alpha
