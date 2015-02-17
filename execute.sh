#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 250 500
	do
	    mkdir -p results/${algorithm}
	    ./mcms.py --migration ${algorithm} --outdir results/${algorithm}/ --simTime 1500 --numThreads ${nT} --numCores 8 --deltaSP 10 $@ &
	done
done
wait

