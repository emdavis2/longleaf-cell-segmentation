#!/bin/bash

for i in {6..36}
do
sbatch run_test.slurm $i
done