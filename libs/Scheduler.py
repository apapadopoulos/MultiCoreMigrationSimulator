import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import copy as cp

import sys

import libs.Process as proc
import libs.Controller as ctrl


class Scheduler(object):
	"""docstring for Scheduler"""
	def __init__(self, name):
		self.name = name

class IplusPI(Scheduler):
	"""docstring for IplusPI"""

	def __init__(self, ident, Kiin=0.25, Kpout=2.5, Kiout=0.5):
		self.id = ident
		self.InnerControllers = []
		self.numReg = 0
		self.outerController = ctrl.PI(ident=self.id,Kp = Kpout, Ki = Kiout)
		self.tauto  = np.zeros(self.numReg)
		self.tauts  = np.zeros(self.numReg)
		self.taur   = np.sum(self.tauts)
		self.alphas = np.zeros(self.numReg)
		self.alphasEff = np.zeros(self.numReg)
		self.Kiin   = Kiin
		self.Kpout  = Kpout
		self.Kiout  = Kiout

		# if self.numReg > 0:
		# 	for i in xrange(0,self.numReg):
		# 		self.InnerControllers.append(ctrl.I(name='InnerController'+str(i), Ki = Kiin, uMin=0))

	def schedule(self,processList,tauro):
		# Check if I have already a controller for each thread in processList
		vidProc = []
		for i in xrange(0,len(processList)):
			ident = processList[i].getID()
			idx   = self.findReg(ident)
			if idx == -1:
				self.addReg(processList[i])
			vidProc.append(ident)

		# Removing the unnecessary regulators
		
		vidReg = [self.InnerControllers[i].getID() for i in xrange(0,self.numReg)]
		toElim = [reg for reg in vidReg if reg not in vidProc]
		for i in toElim:
			# print toElim
			self.removeReg(i)


		# At this point I should have numReg = len(processList)
		if self.numReg != len(processList):
			print '[Scheduler%d] Error! I do not have the right amount of controllers! %d!=%d'%(self.id,self.numReg,len(processList))
			sys.exit()

		#########################
		# Computing the schedule
		#########################
		# Compute the taur
		self.taur = np.sum(self.tauts)

		# Considering the idle time
		if self.taur < tauro:
			self.taur = tauro
			self.bc = 0
			self.outerController.resetU()
		else:
			self.bc = self.outerController.computeU(tauro,self.taur)


		# Schedule all the processes
		for i in xrange(0,len(processList)):
			idxReg = self.findReg(processList[i].getID())
			self.alphas[idxReg] = processList[i].getAlpha()
			self.tauto[idxReg]  = (self.bc + self.taur)*self.alphas[idxReg]
			self.tauts[idxReg]  = processList[i].getY()
			b = self.InnerControllers[idxReg].computeU(self.tauto[idxReg],self.tauts[idxReg])
			processList[i].setU(b)


		self.alphasEff = self.tauts/self.taur


		return np.sum(self.tauts), self.tauts, self.tauto

	def setAlphas(self,alphas):
		if len(alphas) == self.numReg:
			self.alphas = alphas

	def getTauts(self):
		return self.tauts

	def getTauto(self):
		return self.tauto

	def getTaur(self):
		return self.taur

	def findReg(self,ident):
		# Returns the index of the regulator with a id = ident
		# returns -1 if the regulator is not found
		for i in xrange(0,self.numReg):
			if self.InnerControllers[i].getID()==ident:
				return i
		return -1

	def addReg(self,process):
		self.numReg += 1
		self.InnerControllers.append(ctrl.I(ident=process.getID(),Ki=self.Kiin,uMin=0))
		print '[Scheduler%d] Added regulator with id = %d'%(self.id,process.getID())
		self.tauto = np.append(self.tauto,0)
		self.tauts = np.append(self.tauts,0)
		self.taur  = np.sum(self.tauts)
		self.alphas = np.append(self.alphas,process.getAlpha())
	
	def removeReg(self,ident):
		idx = self.findReg(ident)
		if idx != -1:
			ident = self.InnerControllers[idx].getID()
			self.InnerControllers.pop(idx)
			self.tauto = np.delete(self.tauto,idx)
			self.tauts = np.delete(self.tauts,idx)
			self.taur  = np.sum(self.tauts)
			self.alphas = np.delete(self.alphas,idx)
			self.numReg = len(self.InnerControllers)
			print '[Scheduler%d] Removed regulator with id = %d'%(self.id,ident)
		else:
			print '[Scheduler%d] Cannot remove Regulator with id = %d'%(self.id,ident)

	def computeAlphasEff(self):
		return self.alphasEff

	def getNominalUtilization(self):
		U = np.sum(self.alphas)
		return U

	def getUtilization(self):
		U = np.sum(self.computeAlphasEff())
		return U

	def viewUtilization(self):
		print '[Scheduler%d] NominalUtilization = %g\tActualUtilization = %g'%(self.id,self.getNominalUtilization(),self.getUtilization())


	
		

