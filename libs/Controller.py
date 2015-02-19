import numpy as np
import scipy as sp

## TODOs:
#  - re-write all the for loops in a more efficient way
#  - better exploit inheritance

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

	def getID(self):
		return self.id


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

class PI(Controller):
	"""PI controller with transfer function
	   R(z) = Kp + Ki/(z-1)
	"""

	def __init__(self, ident, Kp, Ki,uMin=np.nan,uMax=np.nan):
		self.id   = ident
		self.Kp   = Kp
		self.Ki   = Ki

		# Signals
		self.u    = 0
		self.e    = 0
		self.y    = 0

		# States
		self.eOld = 0

		# Saturations
		self.uMin = uMin
		self.uMax = uMax


	def limit(self,u):
		# Apply saturations
		return np.nanmax([np.nanmin([u,self.uMax]),self.uMin])

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



class I(PI):
	"""Integral controller with trasnfer function
	   R(z) = Ki/(z-1)
	"""

	def __init__(self, ident, Ki,uMin=np.nan,uMax=np.nan):
		self.id   = ident
		self.Kp   = 0
		self.Ki   = Ki
		# Signals
		self.u    = 0
		self.e    = 0
		self.y    = 0

		# Saturations
		self.uMin = uMin
		self.uMax = uMax

	def computeU(self,yo,y):
		self.yo = yo;
		self.y  = y;
		self.e  = yo - y;
		self.u  = self.u + self.Ki*self.e
		self.u  = self.limit(self.u)


		return self.u


