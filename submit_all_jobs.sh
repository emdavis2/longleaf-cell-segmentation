#!/bin/bash

IMG_PATH='/proj/telston_lab/projects/data/reformatted/2023_04_19_StiffGel'

for i in {0..35}
do
sbatch membrane_submitjob.sh $i $IMG_PATH
sleep 0.3
sbatch nucleus_submitjob.sh $i $IMG_PATH
sleep 0.3
done