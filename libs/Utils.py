import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import copy as cp

import libs.Process as proc

import sys
import os
import errno


def addProcess(procList,ident=None, alpha=1,stdDev=0.01):
	numThreads = len(procList)
	if ident == None:
		idproc = numThreads
	else:
		idproc = ident

	# Checking for replicated ids
	pIDs = [procList[i].getID() for i in range(0,numThreads)]
	if idproc not in pIDs:
		procList.append(proc.Process(ident=idproc,\
			                         alpha=alpha,\
		    	                     stdDev=stdDev))
		numThreads = len(procList) + 1
	else:
		print 'Cannot add a process with ID %d'%idproc
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

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def save_results(path, M, header=None):
	# Saving a csv file
	np.savetxt(path, M, delimiter=',',header=header)

def progress(val,end_val, bar_length=20):
    percent = float(val) / end_val
    hashes = '#' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()