#!/usr/bin/python
from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import argparse
import os
import sys

import libs.Process as proc
import libs.Controller as ctrl
import libs.Scheduler as sched
import libs.Migration as mig
import libs.Utils as ut
import libs.Tests as tst


def main():
	## TODOs: 
	#  - add argv with numCores, numThreads, tFin from commandLine
	#  - add print on a file results
	#  - re-write for loops in a more efficient way

	## Manage command line inputs

	# Defining command line options to find out the algorithm
	parser = argparse.ArgumentParser( \
		description='Run multicore migration simulator.', \
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	migrAlgos = ("simple load_aware load_normalized").split()

	parser.add_argument('--migration',
		help = 'Migration algorithm: ' + ' '.join(migrAlgos),
		default = migrAlgos[0])
	parser.add_argument('--outdir',
		help = 'Destination folder for results and logs',
		default = '.')

	parser.add_argument('--simTime',
		type = int,
		help = 'Simulation time.',
		default = 1000)

	parser.add_argument('--numThreads',
		type = int,
		help = 'Number of threads.',
		default = 500)

	parser.add_argument('--numCores',
		type = int,
		help = 'Number of threads.',
		default = 8)

	# Parsing the command line inputs
	args = parser.parse_args()

	# Migration algorithm
	migration = args.migration
	if migration not in migrAlgos:
		print "Unsupported algorithm %s"%format(migration)
		parser.print_help()
		quit()


	## The program starts here
	numCores = args.numCores
	numThreads = args.numThreads
	tFin = args.simTime

	## Creating numThreads threads
	Threads = []
	alphas  = []
	for i in xrange(0,numThreads):
		alpha = 0.5*numCores/numThreads
		alphas.append(alpha)
		ut.addProcess(Threads,ident=i, alpha=alpha,stdDev=0.01)
		Threads[i].viewProcess()
	alphas = np.array(alphas)

	## Creating one scheduler for each core
	Schedulers = []
	tauro      = np.zeros(numCores)
	for i in xrange(0,numCores):
		Schedulers.append(sched.IplusPI(ident=i, Kiin=0.25, Kpout=2.0, Kiout=0.25))
		tauro[i] = 1

	## Creating a migration manager
	# Migration data
	utilizationSetPoint  = 1.0 * np.ones(numCores)  # utilization set point for each core
	relocationThresholds = 0.5 * np.ones(numCores)  # 
	DeltaSP = 20
	mm = mig.MigrationManager(numCores, relocationThresholds, minLoad=0.1)

	placement_matrix = np.zeros((numThreads, numCores));  # how the threads are partitioned among the different cores
	# The threads start all on the first core
	placement_matrix[:,0] = 1;

	# # Partition of the threads among different cores cores
	# placement_matrix[0:numThreads/3, 0] = 1;
	# placement_matrix[numThreads/3+1:2*numThreads/3, -2] = 1;
	# placement_matrix[2*numThreads/3+1:-1, -1] = 1;

	vU  = np.zeros((tFin,numCores))
	vUn = np.zeros((tFin,numCores))
	vSP = np.zeros(tFin)

	## Starting the simulation
	for kk in xrange(1,tFin+1):
		print 'Time %d'%kk
		# If DeltaSP is elapsed, update the utilization set point
		if np.mod(kk,DeltaSP)==0:
			utilizationSetPoint = mm.normalize_load(Schedulers)
		vSP[kk-1] = utilizationSetPoint[0]
		for cc in xrange(0,numCores):
			# Extracting the subset of tasks to be scheduled
			subset_idx = np.nonzero(placement_matrix[:,cc])[0]
			subset_Threads = [Threads[i] for i in subset_idx]
			# Schedule the subset of tasks
			taur, taut, tauto = Schedulers[cc].schedule(subset_Threads,tauro[cc])
			#Schedulers[cc].viewUtilization()
			vU[kk-1,cc]  = Schedulers[cc].getUtilization()
			vUn[kk-1,cc] = Schedulers[cc].getNominalUtilization()
		#placement_matrix = mm.migration_simple(Schedulers, placement_matrix,utilizationSetPoint)
		placement_matrix = mm.migration_load_aware(Schedulers, placement_matrix,utilizationSetPoint,alphas)

	mm.viewTotalMigrations()

	plt.figure(1)
	plt.plot(xrange(0,tFin),vU)
	plt.legend(['Core'+str(i) for i in xrange(0,numCores)])
	plt.plot(xrange(0,tFin),vSP,'--')

	plt.figure(2)
	plt.plot(xrange(0,tFin),vUn)
	plt.plot(xrange(0,tFin),vSP,'--')
	plt.show()







def tests():
	tFin = 500
	numThreads=50
	tst.testInnerLoop(tFin);
	tst.testSchedulerAddRemoveThreads(tFin,numThreads)
	tst.testSchedulerWithInternalDataPlot(tFin,numThreads)
	tst.testSchedulerNoThreads(tFin)


if __name__ == "__main__":
    sys.exit(main())
