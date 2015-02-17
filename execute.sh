#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 250 500
	do
		for rT in 0.1 0.2 0.5
		do
		    mkdir -p results/${algorithm}
		    ./mcms.py --migration ${algorithm} --outdir results/${algorithm}/ --simTime 1500 --numThreads ${nT} --numCores 8 --deltaSP 10 --relocationThreshold ${rT} $@ &
		done
	done
done
wait

