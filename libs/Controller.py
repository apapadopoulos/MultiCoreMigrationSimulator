import numpy as np
import scipy as sp

class Controller:
	""" Definition of a Controller
	    Computes a control action according to a control law
	    u(k+1) = f(u,yo,y)
	    where
	    - u is the control signal
	    - yo is the set point
	    - y is the measured output
	"""
	def __init__(self, ident):
		self.id = ident

class PID(Controller):
	"""docstring for PID"""

	def __init__(self, ident, K, Ti, Td, Beta=1, N=10):
		self.id   = ident
		self.K    = K
		self.Ti   = Ti
		self.Td   = Td
		self.Beta = Beta
		self.Tr   = Tr
		self.N    = N
		self.ad   = Td / (Td + N)
		self.bd   = K*self.ad*N
		# Signals
		self.u    = 0
		self.e    = 0
		self.y    = 0
		# States
		self.D    = 0
		self.I    = 0
		self.yOld = 0

	def computeU(self,yo,y):
		self.yo = yo;
		self.y  = y;
		self.e  = yo - y;
		self.D  = self.ad*self.D - self.bd*(y-self.yOld)
		self.u  = self.K*(self.Beta*yo - y) + self.I + self.D

		# updateStatus
		self.I = self.I + self.K/self.Ti*self.e
		self.yOld = self.y;

	def getID(self):
		return self.id

class PI(Controller):
	"""PI controller with transfer function
	   R(z) = Kp + Ki/(z-1)
	"""

	def __init__(self, ident, Kp, Ki,uMin=None,uMax=None):
		self.id   = ident
		self.Kp   = Kp
		self.Ki   = Ki
		# Signals
		self.u    = 0
		self.e    = 0
		self.y    = 0
		# States
		self.eOld = 0

		self.uMin = uMin
		self.uMax = uMax


	def limit(self,u):
		if self.uMin == None:
			if self.uMax == None:
				return u
			else:
				return np.min(u,self.uMax)
		else:
			if self.uMax == None:
				return np.max(u,self.uMin)
			else:
				return np.max(np.min(u,self.uMax),self.uMin)


	def computeU(self,yo,y):
		self.yo = yo;
		self.y  = y;
		self.e  = yo - y;
		self.u  = self.u + self.Kp*(self.e - self.eOld) + self.Ki*self.e
		self.u  = self.limit(self.u)

		# updateStatus
		self.eOld = self.e;

		return self.u

	def resetU(self,newU=0):
		self.u = newU

	def getKp(self):
		return self.Kp

	def getKi(self):
		return self.Ki

	def getID(self):
		return self.id



class I(Controller):
	"""Integral controller with trasnfer function
	   R(z) = Ki/(z-1)
	"""

	def __init__(self, ident, Ki,uMin=None,uMax=None):
		self.id   = ident
		self.Ki   = Ki
		# Signals
		self.u    = 0
		self.e    = 0
		self.y    = 0


		self.uMin = uMin
		self.uMax = uMax

	def limit(self,u):
		if self.uMin == None:
			if self.uMax == None:
				return u
			else:
				return np.min(u,self.uMax)
		else:
			if self.uMax == None:
				return np.max(u,self.uMin)
			else:
				return np.max(np.min(u,self.uMax),self.uMin)

	def computeU(self,yo,y):
		self.yo = yo;
		self.y  = y;
		self.e  = yo - y;
		self.u  = self.u + self.Ki*self.e
		self.u  = self.limit(self.u)


		return self.u

	def getKi(self):
		return self.Ki

	def getID(self):
		return self.id


