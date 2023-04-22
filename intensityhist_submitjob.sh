#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem=50g
#SBATCH -p general
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=
#SBATCH -o %j.out
#SBATCH -e err.%j

python ./GenerateIntensityHistogram.py '/proj/telston_lab/projects/data/reformatted/2023_04_19_Glass' '/nas/longleaf/home/emae/Segmentation/figures'
