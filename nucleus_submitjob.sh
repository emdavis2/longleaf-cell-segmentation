#!/bin/bash

## Set the DATA_PATH to the directory you want the job to run in.
##
## On the singularity command line, replace ./test.py with your program
##
## Change reserved resources as needed for your job.
##

#SBATCH --job-name=tensorflow
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=5g
#SBATCH --time=4:00:00
#SBATCH --partition=volta-gpu
#SBATCH --output=run-%j.log
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_access

unset OMP_NUM_THREADS

# Set SIMG path
SIMG_PATH=/nas/longleaf/apps/tensorflow_py3/2.3.1/simg

# Set SIMG name
SIMG_NAME=tensorflow2.3.1-py3-cuda10.1-ubuntu18.04.simg

# Set data path
DATA_PATH=/nas/longleaf/home/emae/Segmentation

# GPU with Singularity
singularity exec --nv -B /work/users/{o}/{n}/{onyen} -B /proj $SIMG_PATH/$SIMG_NAME bash -c "cd $DATA_PATH; python ./Segment_Images.py $2 $1 '/proj/telston_lab/projects/keras_unet_models/nucleus/keras_unet_model_transfer_nucleus_segmenter_06302023_1024x1024imagesize_model_config.json' '/proj/telston_lab/projects/keras_unet_models/nucleus/keras_unet_model_transfer_nucleus_segmenter_06302023_1024x1024imagesize_weights_only.h5' 'nucleus' 1001 1001"