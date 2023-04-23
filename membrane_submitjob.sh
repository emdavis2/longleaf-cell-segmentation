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
python ./Segment_Images.py '/proj/telston_lab/projects/data/2023_03_30_softgel_s1' '/proj/telston_lab/projects/keras_unet_models/keras_unet_model_cell_segmenter_02152023_3trainingsets_varyingcontrasts_1024x1024imagesize' 'membrane'
