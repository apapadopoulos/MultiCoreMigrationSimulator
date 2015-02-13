import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import sys

import libs.Process as proc
import libs.Controller as ctrl
import libs.Scheduler as sched
import libs.Utils as ut

def testInnerLoop(tFin):
	G = proc.Process(ident=1,alpha=1,stdDev=0.01)
	G.viewProcess()

	R = ctrl.I(ident=G.getID(), Ki=0.25)

	tauto = 0.5

	vtauto = np.zeros((tFin,1))
	vtaut  = np.zeros((tFin,1))

	for kk in xrange(1,tFin+1):
		taut = G.getY()
		u = R.computeU(tauto,taut)
		G.setU(u)

		# Store variables
		vtauto[kk-1,0] = tauto
		vtaut[kk-1,0]  = taut

	plt.plot(xrange(0,tFin),vtaut,'b')
	plt.plot(xrange(0,tFin),vtauto,'k--')
	plt.show()

def testScheduler(tFin,numThreads):
	# Creating numThreads threads
	Threads = []
	alphas  = []
	for i in xrange(0,numThreads):
		alpha = 0.1
		Threads.append(proc.Process(ident=i,alpha=alpha, stdDev = 0.0))
		Threads[i].viewProcess()

	scheduler = sched.IplusPI(ident=0, Kiin=0.25, Kpout=2.0, Kiout=0.25)

	tauro = 1

	vtauro = np.zeros((tFin,1))
	vtaur  = np.zeros((tFin,1))
	vtauto = []
	vtaut  = []

	for kk in xrange(1,tFin+1):

		if kk == 100:
			print 'Adding a process...'
			numThreads = ut.addProcess(Threads,alpha=0.5,ident=100)

		if kk == 200:
			print 'Removing a process...'
			numThreads = ut.removeProcess(Threads,100)

		if kk == 300:
			print 'Adding a process...'
			numThreads = ut.addProcess(Threads,alpha=0.6,ident=100,stdDev=0)

		if kk == 400:
			print 'Removing a process...'
			numThreads = ut.removeProcess(Threads,90)

		if kk == 410:
			print 'Removing a process...'
			numThreads = ut.removeProcess(Threads,100)


		taur, taut, tauto = scheduler.schedule(Threads,tauro)
		scheduler.viewUtilization()

		# Store variables
		vtauro[kk-1,0] = tauro
		vtaur[kk-1,0]  = taur
		vtauto.append(tauto)
		vtaut.append(taut)
		

	plt.plot(xrange(0,tFin),vtaur,'b')
	plt.plot(xrange(0,tFin),vtauro,'k--')
	plt.show()

def testScheduler2(tFin,numThreads):
	# Creating numThreads threads
	Threads = []
	alphas  = []
	for i in xrange(0,numThreads):
		alpha = 1.0/(i+1)
		Threads.append(proc.Process(ident=i,alpha=alpha, stdDev = 0.01))
		Threads[i].viewProcess()

	scheduler = sched.IplusPI(ident=0, Kiin=0.25, Kpout=2.0, Kiout=0.25)

	tauro = 1

	vtauro = np.zeros((tFin,1))
	vtaur  = np.zeros((tFin,1))
	vtauto = np.zeros((tFin,numThreads))
	vtaut  = np.zeros((tFin,numThreads))

	for kk in xrange(1,tFin+1):
		taur, taut, tauto = scheduler.schedule(Threads,tauro)
		scheduler.viewUtilization()

		# Store variables
		vtauro[kk-1,0] = tauro
		vtaur[kk-1,0]  = taur
		vtauto[kk-1,:] = tauto
		vtaut[kk-1,:]  = taut
	
	plt.figure(1)
	plt.plot(xrange(0,tFin),vtaur,'b')
	plt.plot(xrange(0,tFin),vtauro,'k--')

	plt.figure(2)
	plt.plot(xrange(0,tFin),vtaut)
	plt.plot(xrange(0,tFin),vtauto,'--')
	plt.show()
