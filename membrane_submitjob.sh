#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=10:00:00
#SBATCH --mem=40g
#SBATCH -p gpu
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=
#SBATCH -o %j.out
#SBATCH -e err.%j

module add tensorflow_py3/2.1.0
python ./Segment_Images.py '/proj/telston_lab/projects/data/reformatted/2023_04_19_Glass' '1' '/proj/telston_lab/projects/keras_unet_models/keras_unet_model_cell_segmenter_04262023_1024x1024imagesize' 'membrane'
