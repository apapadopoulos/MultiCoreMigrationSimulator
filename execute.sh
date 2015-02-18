#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 250 500 1000
	do
		for pad in 1.0 1.05 1.1 1.2 1.5
		do
			for rT in 0.5 1.0
				for cc in 2 4 8 16 32 64 128
				do
				    mkdir -p results/${algorithm}
				    ./mcms.py --migration ${algorithm} \
				              --outdir results/${algorithm}/ \
				              --numThreads ${nT} \
				              --numCores ${cc} \
				              --padding ${pad} \
				              --relocationThreshold ${rT} \
				              --simTime 1500 \
				              --deltaSP 20 \
				              --startupTime 0\
				              $@ &
				done
			done
		done
		wait
	done
done


