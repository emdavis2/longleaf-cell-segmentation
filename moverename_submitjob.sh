#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem=50g
#SBATCH -p general
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=
#SBATCH -o %j.out
#SBATCH -e err.%j

python ./Move_Rename.py '/proj/telston_lab/projects/data/2023_08_26_Jr20RandomMigrationPDMS/10x_JR20_PDMS_Overnight' '/proj/telston_lab/projects/data/reformatted' '2023_08_26_JR20RandomMigrationPDMS'