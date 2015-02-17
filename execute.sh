#!/bin/bash

rm -rf results
mkdir -p results

algs=( simple load_aware load_normalized )

for algorithm in "${algs[@]}"
do
    mkdir -p results/${algorithm}
    ./mcms.py --migration ${algorithm} --outdir results/${algorithm}/ --simTime 1500 --numThreads 500 --numCores 8 --deltaSP 10 $@ &
done
wait

