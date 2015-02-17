#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 #250 500
	do
		for rT in 0.1 #0.2 0.5 1.0
		do
			for cc in 8 #16 32
			do
			    mkdir -p results/${algorithm}
			    ./mcms.py --migration ${algorithm} --outdir results/${algorithm}/ --simTime 1000 --numThreads ${nT} --numCores ${cc} --deltaSP 10 --relocationThreshold ${rT} $@ &
			done
		done
	done
done
wait

