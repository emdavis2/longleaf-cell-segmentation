Cell Segmentation on UNC Longleaf Cluster
================
## Quick Summary:
This repo contains code to perform binary mask generation of DIC images of JR20 dermal fibroblast cells through the use of a CNN run using a GPU. Specifically, this repo contains instructions for running the code on the UNC Longleaf cluster. 

The file `PreprocessImages.ipynb` is a Jupyter notebook that is to be run using the Open OnDemand access to the longleaf cluster (<https://help.rc.unc.edu/ondemand>) and it's purpose is to preprocess the images to ensure that the intensites are appropriately rescaled and the images are 8 bit and in RGB format as well as ensuring the dimensions are square (if dimensions are not square, padding with zeros is performed).

The file `Segment_Images.py` is a python script that uses a CNN model saved with keras to segment the preprocessed DIC images, make a directory where the images are located and saves the masks there. It uses the GPU node on the Longleaf cluster and it takes in three agruments: the path where the saved keras model is saved, the path where the preprocessed DIC images to be segmented are located, and the type of mask that is being generated (membrane or nucleus).

`membrane_submitjob.sh` is a SLURM job submission script to use the pretrained keras membrane CNN model to segment membrane and `nucleus_submitjob.sh` is a SLURM job submission script to use the pretrained keras nucleus CNN model to segment nucleus. Before running these files, the second string in the last line needs to be changed to denote the path to where the preprocessed images are located.

A required folder is `keras_unet_models`, as it contains the trained CNN models (saved with keras) which are used to segment the cell membrane and cell nucleus. There are 2 models in this folder: one for membrane and one for nucleus. Currently this folder is located on the following path: `/proj/telston_lab/projects/keras_unet_models`. *Note: You must have access to the `/proj/telston_lab` space to access this folder.*

## Set up to run code:
Clone this repository to your home directory on the Longleaf cluster. To run segmentation, you must have access to the GPU partition on Longleaf. If you do not already have access to the Longleaf GPUs, email research@unc.edu to request access.

Within the `.sh` slurm job submission scripts, there is just one attribute that needs to be modified at setup: your email on the line `#SBATCH --mail-user=` to receive emails when your job runs, finishes running, or fails. Make sure to do this for both `membrane_submitjob.sh` and `nucleus_submitjob.sh`. 

## Workflow for a dataset:
### Step 1: Preprocessing

The first step for image segmentation will be to run the `PreprocessImages.ipynb` notebook to preprocess the images. To do this, log on to OnDemand (<https://help.rc.unc.edu/ondemand>) and open the Jupyter Notebook application. You will be prompted to enter some parameters for your interactive session. For time, I recommend entering 5 hours and for Additional Job Submission Arguments I recommend requesting 50gb of memory (this would be typed as `--mem=50gb`). For number of CPU, just enter 1. You can now click launch and your request will be sent through on the queue (usually doesn't take long, but it does depend on the amount of resources you request). Once your session is started you can click "connect to Jupyter" and it will launch to the launcher homepage. On the left hand side you should see directories in your home directory on Longleaf (if you did not enter a path in the Jupyter startup directory field when requesting the session). Navigate to where this repo is cloned and open `PreprocessImages.ipynb`. Make sure the Python 3 (ipykernal) is selected for the kernal (that should be the default).

There are only 3 variables that need to be changed within this notebook: `image_path` (located in code block 2), `min_val` and `max_val` (both located in code block 5). `image_path` is the path to where the images you wish to preprocess are located on the Longleaf cluster. `min_val` and `max_val` are variables that you need to enter based upon the histogram of image intensites generated in code block 4. The output of this notebook is images that are resaved in the appropriate format in the same location from which they were located originally (CAUTION: the original images will be rewritten).

### Step2: Segmentation

Once you have the preprocessed images, they are now ready for segmentation. Log into Longleaf and navigate to the directory where this cloned repo is located. To segment, there is only 1 attribute that needs to be changed in both `membrane_submitjob.sh` and `nucleus_submitjob.sh`: the first argument after `python ./Segment_Images.py`, which is the path to the images. Simply change this path to the appropriate path of where the preprocessed images you wish to segment are located. *Note: the first argument is the path to the directory where the DIC images are located, the second argument is the path to the saved keras model to apply in the `keras_unet_models` folder, the thrid argument is the feature of interest to segment.* To segment the cell membrane, simply type: 

```
sbatch membrane_submitjob.sh
``` 

into the command line (make sure once again you are in the directory of this cloned repo for this command to work). Similarly, to segment cell nucleus, type:

```
sbatch nucleus_submitjob.sh
```

 You can segment both membrane and nucleus at the same time by entering the commands back to back.



