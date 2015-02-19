import numpy as np
import scipy as sp
import random

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
    sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()

def argMaxSet(vec):
	# Find all the indices with maximum value
	max_val = np.max(vec)
	indices = [i for i in xrange(0,len(vec)) if vec[i]==max_val]
	return indices

def argMinSet(vec):
	# Find all the indices with minimum value
	min_val = np.min(vec)
	indices = [i for i in xrange(0,len(vec)) if vec[i]==min_val]
	return indices

def argMaxRand(vec):
	# Find the index with maximum value. If there is more than one
	# a random index is chosen
	indices = argMaxSet(vec)
	index = random.choice(indices)
	return index

def argMaxFirst(vec):
	# Find the index with maximum value. If there is more than one
	# the first one is chosen
	indices = argMaxSet(vec)
	index = indices[0]
	return index

def argMaxLast(vec):
	# Find the index with maximum value. If there is more than one
	# the first one is chosen
	indices = argMaxSet(vec)
	index = indices[-1]
	return index

def argMinRand(vec):
	# Find the index with maximum value. If there is more than one
	# a random index is chosen
	indices = argMinSet(vec)
	index = random.choice(indices)
	return index

def ewma(vec,y,alpha=0.05):
	res = alpha*vec + (1-alpha)*y
	return res

def ma(vec,y,n):
	if n <= 0:
		return y
	else:
		return (vec * n + y)/(n+1)

def jainIndex(x):
	n = len(x);
	squared_sum = np.sum(x)**2
	sum_squared = np.sum(x**2)
	if sum_squared > 0:
		return squared_sum/(n*sum_squared);
	else:
		return 0.0