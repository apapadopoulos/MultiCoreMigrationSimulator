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
		default = './results/')

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

	parser.add_argument('--utilizationSetPoint',
		type = float,
		help = 'Utilization setpoint.',
		default = 0.5)
	
	parser.add_argument('--relocationThreshold',
		type = float,
		help = 'Relocation threashold.',
		default = 0.5)

	parser.add_argument('--deltaSP',
		type = int,
		help = 'Set point update period (Valid only with load_normalized!).',
		default = 10)

	parser.add_argument('--padding',
		type = float,
		help = 'Padding for the adaptation of the set point (Valid only with load_normalized!).',
		default = 1.0)

	parser.add_argument('--startupTime',
		type = int,
		help = 'Time needed for the system to startup.',
		default = 0)

	parser.add_argument('--plot',
		type = int,
		help = 'Option to show graphs or not.',
		default = 0)

	parser.add_argument('--save',
		type = int,
		help = 'Options to save data or not.',
		default = 1)

	parser.add_argument('--verb',
		type = int,
		help = 'Options to have a verbose execution.',
		default = 0)

	# Parsing the command line inputs
	args = parser.parse_args()

	# Migration algorithm
	migration = args.migration
	if migration not in migrAlgos:
		print "Unsupported algorithm %s"%format(migration)
		parser.print_help()
		quit()
	# Creating the directory where to store the results
	ut.mkdir_p(args.outdir)

	##############################
	## The program starts here
	##############################
	numCores = args.numCores
	numThreads = args.numThreads
	tFin = args.simTime

	## Creating numThreads threads
	Threads = []
	alphas  = []
	for i in xrange(0,numThreads):
		alpha = 0.5*numCores/numThreads
		alphas.append(alpha)
		ut.addProcess(Threads,ident=i, alpha=alpha,stdDev=0.005)
		# Threads[i].viewProcess()
	alphas = np.array(alphas)

	## Creating one scheduler for each core
	Schedulers = []
	tauro      = np.zeros(numCores)
	for i in xrange(0,numCores):
		Schedulers.append(sched.IplusPI(ident=i, Kiin=0.25, Kpout=2.0, Kiout=0.25))
		tauro[i] = 1

	## Creating a migration manager
	# Migration data
	utilizationSetPoint  = args.utilizationSetPoint * np.ones(numCores)  # utilization set point for each core
	relocationThresholds = args.relocationThreshold * np.ones(numCores)  # Thresholds
	DeltaSP = args.deltaSP
	mm = mig.MigrationManager(numCores, relocationThresholds, minLoad=0.1, padding=args.padding, verb=False)

	placement_matrix = np.zeros((numThreads, numCores));  # how the threads are partitioned among the different cores
	# The threads start all on the first core
	placement_matrix[:,0] = 1;


	vkk = np.zeros((tFin,1))
	vSP = np.zeros((tFin,numCores))
	vUn = np.zeros((tFin,numCores))
	vU  = np.zeros((tFin,numCores))
	vmig= np.zeros((tFin,1))
	vOI = np.zeros((tFin,numCores))

	## Starting the simulation
	print '[%s] started with:\n\tnumCores=%d,\n\tnumThreads=%d,\n\tpadding=%f,\n\trelocationThreshold=%f,\n\ttFin=%d...'%\
	            (args.migration,\
				 args.numCores,\
				 args.numThreads,\
				 args.padding,\
	             args.relocationThreshold,\
				 args.simTime)

	for kk in xrange(1,tFin+1):
		if args.verb:
			ut.progress(kk,tFin, bar_length=20)

		vkk[kk-1,:] = kk
		for cc in xrange(0,numCores):
			# Extracting the subset of tasks to be scheduled
			subset_idx = np.nonzero(placement_matrix[:,cc])[0]
			subset_Threads = [Threads[i] for i in subset_idx]
			# Schedule the subset of tasks
			taur, taut, tauto = Schedulers[cc].schedule(subset_Threads,tauro[cc])
			#Schedulers[cc].viewUtilization()
			vU[kk-1,cc]  = Schedulers[cc].getUtilization()
			vUn[kk-1,cc] = Schedulers[cc].getNominalUtilization()

		vOI[kk-1,:] = mm.getOverloadIndex()

		if kk > args.startupTime:
			# Apply migration algorithm
			if migration=='simple':
				placement_matrix = mm.migration_simple(Schedulers, placement_matrix,utilizationSetPoint)
			elif migration=='load_aware':
				placement_matrix = mm.migration_load_aware(Schedulers, placement_matrix,utilizationSetPoint,alphas)
			elif migration=='load_normalized':
				# If DeltaSP is elapsed, update the utilization set point
				if np.mod(kk,DeltaSP)==0:
					utilizationSetPoint = mm.normalize_load(Schedulers)
				else:
					mm.average_load(Schedulers)
				placement_matrix = mm.migration_load_aware(Schedulers, placement_matrix,utilizationSetPoint,alphas)

		# Saving the utilization setpoint
		vSP[kk-1,:] = utilizationSetPoint
		vmig[kk-1,:] = mm.getTotalMigrations()
	if args.verb:
		print '\nSimulation finished!\n'
		mm.viewTotalMigrations()
	print '[%s] finished sim with:\n\tnumCores=%d,\n\tnumThreads=%d,\n\tpadding=%f,\n\trelocationThreshold=%f,\n\ttFin=%d...'%\
	          (args.migration,\
			   args.numCores,\
			   args.numThreads,\
			   args.padding,\
			   args.relocationThreshold,\
			   args.simTime)

	if args.plot:
		plt.figure(1)
		plt.plot(xrange(0,tFin),vU)
		plt.legend(['Core'+str(i) for i in xrange(0,numCores)])
		plt.plot(xrange(0,tFin),vSP,'--')

		plt.figure(2)
		plt.plot(xrange(0,tFin),vUn)
		plt.plot(xrange(0,tFin),vSP,'--')

		plt.figure(3)
		plt.plot(xrange(0,tFin),vOI)
		plt.plot(xrange(0,tFin),args.relocationThreshold*np.ones(tFin),'k--')
		plt.show()

	if args.save:
		# Saving results in the outdir directory
		header = 'Round,'
		for cc in xrange(0,numCores):
			header += 'SetPointUtilization'+str(cc)+','
		for cc in xrange(0,numCores):
			header += 'NominalUtilizationCore'+str(cc)+','
		for cc in xrange(0,numCores):
			header += 'UtilizationCore'+str(cc)+','
		for cc in xrange(0,numCores):
			header += 'OverloadIndex'+str(cc)+','
		header += 'TotalMigrations'

		M      = np.hstack((vkk,vSP,vUn,vU,vOI,vmig))
		ut.save_results(args.outdir+'results_'\
								   +migration+'_'\
			 					   +'numCores'+str(numCores)+'_'\
								   +'numThreads'+str(numThreads)+'_'\
								   +'padding'+str(args.padding)+'_'\
								   +'relocationThreshold'+str(args.relocationThreshold)\
								   +'.csv', M, header=header)


def tests():
	tFin = 500
	numThreads=50
	tst.testInnerLoop(tFin);
	tst.testSchedulerAddRemoveThreads(tFin,numThreads)
	tst.testSchedulerWithInternalDataPlot(tFin,numThreads)
	tst.testSchedulerNoThreads(tFin)


if __name__ == "__main__":
    sys.exit(main())
