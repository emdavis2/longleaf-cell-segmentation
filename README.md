Cell Segmentation on UNC Longleaf Cluster
================
## Quick Summary:
This repo contains code to perform binary mask generation of DIC images of JR20 dermal fibroblast cells through the use of a CNN run using a GPU. Specifically, this repo contains instructions for running the code on the UNC Longleaf cluster. 

The file `PreprocessImages.ipynb` is a Jupyter notebook that is to be run using the Open OnDemand access to the longleaf cluster (<https://help.rc.unc.edu/ondemand>) and it's purpose is to preprocess the images to ensure that the intensites are appropriately rescaled and the images are 8 bit and in RGB format as well as ensuring the dimensions are square (if dimensions are not square, padding with zeros is performed).

The file `Segment_Images.py` is a python script that uses a CNN model saved with keras to segment the preprocessed DIC images, make a directory where the images are located and saves the masks there. It uses the GPU node on the Longleaf cluster and it takes in three agruments: the path where the saved keras model is saved, the path where the preprocessed DIC images to be segmented are located, and the type of mask that is being generated (membrane or nucleus).

`membrane_submitjob.sh` is a SLURM job submission script to use the pretrained keras membrane CNN model to segment membrane and `nucleus_submitjob.sh` is a SLURM job submission script to use the pretrained keras nucleus CNN model to segment nucleus. Before running these files, the second string in the last line needs to be changed to denote the path to where the preprocessed images are located.

## Set up to run code:
Clone this repository and place it in your home directory on the Longleaf cluster.

Before running the code, a conda environment needs to be created which can be done via the .yml file. Additionally, you must make sure 

## How to Run:
Clone this repository and place it in your home directory on the Longleaf cluster.

```
sbatch membrane_submitjob.sh
```

```
sbatch nucleus_submitjob.sh
```