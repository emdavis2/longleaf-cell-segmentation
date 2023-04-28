#!/bin/bash

for i in {6..36}
do
sbatch membrane_submitjob.sh $i
sbatch nucleus_submitjob.sh $i
done