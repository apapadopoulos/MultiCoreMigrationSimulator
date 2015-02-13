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

	tst.testScheduler(tFin,numThreads)

	# # Creating numThreads threads
	# Threads = []
	# alphas  = []
	# for i in xrange(0,numThreads):
	# 	alpha = 1.0/2**i
	# 	alphas.append(alpha)
	# 	Threads.append(proc.Process(ident=i, alpha=alpha, stdDev = 0.0))
	# 	Threads[i].viewProcess()
	# alphas = np.array(alphas)

	# placement_matrix = np.zeros((numThreads, numCores));
	# placement_matrix[:, 0] = 1; # in the beginning all threads are on the first core
	# integrated_overload_index = np.zeros((1, numCores)); # init overload index

	# AA = np.tile(alphas,[numCores,1]).T # The equivalent of repmat in Matlab
	# Alphas = AA*placement_matrix


	# # Creating one scheduler for each core
	# Schedulers = []
	# tauro      = np.zeros(numCores)
	# for i in xrange(0,numCores):
	# 	aa  = Alphas[:,i]
	# 	idx = np.nonzero(aa)[0]
	# 	aa  = aa[idx]
	# 	Schedulers.append(sched.IplusPI(name='IplusPI',\
	# 		                            numProc=len(aa),\
	# 		                            alphas=aa,\
	# 		                            Kiin=0.25,\
	# 		                            Kpout=2,\
	# 		                            Kiout=0.05))
	# 	tauro[i] = 1

	# vtauro = np.zeros((tFin,1))
	# vtaur  = np.zeros((tFin,1))
	# vtauto = np.zeros((tFin,numThreads))
	# vtaut  = np.zeros((tFin,numThreads))








def tests():
	tFin = 500
	numThreads=50
	tst.testInnerLoop(tFin);
	tst.testScheduler(tFin,numThreads)
	tst.testScheduler2(tFin,numThreads)


if __name__ == "__main__":
    sys.exit(main())
