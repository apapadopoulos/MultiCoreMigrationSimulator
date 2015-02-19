#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
	for nT in 100 128 250 256 500 512 1000 1024 2000 2048
	do
		for pad in 1.0
		do
			for rT in 0.5
			do
				for cc in 2 4 8 16 32 64 128 256
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
				              --scenario 0\
				              $@ &
				done
			done
		done
	done
done
wait

