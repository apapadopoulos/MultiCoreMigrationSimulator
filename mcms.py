#!/usr/bin/python
from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import sys

import libs.Process as proc
import libs.Controller as ctrl
import libs.Scheduler as sched
import libs.Utils as ut
import libs.Tests as tst


def main():
	numCores = 2
	numThreads = 5
	tFin = 500

	## Creating numThreads threads
	Threads = []
	alphas  = []
	for i in xrange(0,numThreads):
		alpha = 0.5
		alphas.append(alpha)
		ut.addProcess(Threads,ident=i, alpha=alpha,stdDev=0.0)
		Threads[i].viewProcess()
	alphas = np.array(alphas)

	## Creating one scheduler for each core
	Schedulers = []
	tauro      = np.zeros(numCores)
	for i in xrange(0,numCores):
		Schedulers.append(sched.IplusPI(ident=i, Kiin=0.25, Kpout=2.0, Kiout=0.25))
		tauro[i] = 1


	## Migration data

	total_migrations = 0;  # counter for the number of migrations

	utilizationSetPoint  = 0.60 * np.ones((numCores))  # utilization set point for each core
	relocationThresholds = 1.10 * utilizationSetPoint  # 

	placement_matrix = np.zeros((numThreads, numCores));  # how the threads are partitioned among the different cores
	placement_matrix[:, 0] = 1; # in the beginning all threads are on the first core
	integrated_overload_index = np.zeros((1, numCores)); # init overload index

	AA = np.tile(alphas,[numCores,1]).T # The equivalent of repmat in Matlab
	Alphas = AA*placement_matrix

	## Starting the simulation
	for kk in xrange(1,tFin+1):
		# Scheduling all the cores
		if kk == 450:
			# simulating a migration
			placement_matrix[0,0] = 0
			placement_matrix[0,1] = 1
		for cc in xrange(0,numCores):
			# Extracting the subset of tasks to be scheduled
			subset_idx = np.nonzero(placement_matrix[:,cc])[0]
			subset_Threads = [Threads[i] for i in subset_idx]
			# Schedule the subset of tasks
			taur, taut, tauto = Schedulers[cc].schedule(subset_Threads,tauro[cc])
			Schedulers[cc].viewUtilization()


	vtauro = np.zeros((tFin,1))
	vtaur  = np.zeros((tFin,1))
	vtauto = np.zeros((tFin,numThreads))
	vtaut  = np.zeros((tFin,numThreads))








def tests():
	tFin = 500
	numThreads=50
	tst.testInnerLoop(tFin);
	tst.testSchedulerAddRemoveThreads(tFin,numThreads)
	tst.testSchedulerWithInternalDataPlot(tFin,numThreads)
	tst.testSchedulerNoThreads(tFin)


if __name__ == "__main__":
    sys.exit(main())
