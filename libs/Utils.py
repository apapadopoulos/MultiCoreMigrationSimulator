import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import copy as cp

import libs.Process as proc

import sys


def addProcess(procList,ident=None, alpha=1,stdDev=0.01):
	# TODO check on existing ids
	numThreads = len(procList) + 1
	if ident == None:
		idproc = numThreads - 1
	else:
		idproc = ident
	procList.append(proc.Process(ident=idproc,\
		                         alpha=alpha,\
		                         stdDev=stdDev))
	return numThreads


def removeProcess(procList,ident):
	numThreads = len(procList)
	pIDs = [procList[i].getID() for i in range(0,numThreads)]
	if ident in pIDs:
		idx = pIDs.index(ident)
		procList.pop(idx)
		numThreads -= 1
	else:
		print 'Cannot find process with ID = %d'%ident
	return numThreads