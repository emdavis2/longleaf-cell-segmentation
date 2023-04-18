#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --time=3:00:00
#SBATCH --mem=20g
#SBATCH -p gpu
#SBATCH --qos gpu_access
#SBATCH --gres=gpu:1
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=emae@med.unc.edu
#SBATCH -o %j.out
#SBATCH -e err.%j


python ./Segment_Images.py '/nas/longleaf/home/emae/keras_unet_models/keras_unet_model_nucleus_segmenter_02152023_3trainingsets_varyingcontrasts_1024x1024imagesize' '/proj/telston_lab/projects/data/2023_03_30_softgel_s1' 'nucleus'