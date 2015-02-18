#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 250 500 1000
	do
		for pad in 1.0 1.1 1.2 1.5
		do
			for cc in 4 8 16 32 64 128
			do
			    mkdir -p results/${algorithm}
			    ./mcms.py --migration ${algorithm} \
			              --outdir results/${algorithm}/ \
			              --numThreads ${nT} \
			              --numCores ${cc} \
			              --padding ${pad} \
			              --relocationThreshold 0.5 \
			              --simTime 1500 \
			              --deltaSP 20 \
			              $@ &
			done
			wait
		done
	done
done


