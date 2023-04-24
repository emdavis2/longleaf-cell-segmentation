Cell Segmentation on UNC Longleaf Cluster
================
## Quick Summary:
This repo contains code to perform binary mask generation of DIC images of JR20 dermal fibroblast cells through the use of a CNN run using a GPU. Specifically, this repo contains instructions for running the code on the UNC Longleaf cluster. Here is a quick overiew of the files in this repo and what they do:

`Unstack_TiffStacks.py` is a python script that takes a folder of movies that are in tiff stack form and saves them as image sequences instead. The "unstacked" images are saved in a folder called "reformatted" located at the following path `/proj/telston_lab/projects/data/reformatted`. `unstack_submitjob.sh` is a SLURM job submission script to run `Unstack_TiffStacks.py`. Before running, the first and second string in the last line of the SLURM job submission script needs to be changed to denote the location of the folder of tiff stacks and the name of folder to save the unstacked images to in the `/proj/telston_lab/projects/data/reformatted` directory, respectively.

The file `GenerateIntensityHistogram.py` is a python script that makes a histogram of the image intensity values and saves them to a specified folder. This is used as a part of the preprocessing step and used to ensure that the intensities are appropriately rescaled. `intensityhist_submitjob.sh` is a SLURM job submission script to run `GenerateIntensityHistogram.py`. Before running, the first and second string in the last line of the SLURM job submission script needs to be changed to denote the location of the image sequences to generate an intensity histogram from and the path where to save the histogram to, respectively. 

The file `PreprocessImages.py` is a python script that performs the image preprocessing by rescaling the intensities according to the intensity histograms, as well as making sure the images are 8 bit and in RGB format as well as ensuring the dimensions are square (if dimensions are not square, padding with zeros is performed). The preprocessed images overwrite the existing images. `preprocessing_submitjob.sh` is a SLURM job submission script to run `PreprocessImages.py`. Before running, the string in the last line of the SLURM job submission script must be changed to denote the location of the image sequences to be preprocessed and the last two images of the last line need to be changed to the minimum and maximum values of intensity to rescale the images, respectively. The min and max intensity values should be determined from the intensity histogram generated from `GenerateIntensityHistorgram.py`.

The file `Segment_Images.py` is a python script that uses a CNN model saved with keras to segment the preprocessed DIC images, make a directory where the images are located and saves the masks there. It uses the GPU node on the Longleaf cluster and it takes in three arguments: the path where the saved keras model is saved, the path where the preprocessed DIC images to be segmented are located, and the type of mask that is being generated (membrane or nucleus). `membrane_submitjob.sh` is a SLURM job submission script to use the pretrained keras membrane CNN model to segment membrane and `nucleus_submitjob.sh` is a SLURM job submission script to use the pretrained keras nucleus CNN model to segment nucleus. Before running these files, the second string in the last line needs to be changed to denote the path to where the preprocessed images are located.

A required folder is `keras_unet_models`, as it contains the trained CNN models (saved with keras) which are used to segment the cell membrane and cell nucleus. There are 2 models in this folder: one for membrane and one for nucleus. Currently this folder is located on the following path: `/proj/telston_lab/projects/keras_unet_models`. *Note: You must have access to the `/proj/telston_lab` space to access this folder.*

Note: `Unstack_TiffStacks.py`, `GenerateIntensityHistogram.py`, and `PreprocessImages.py` are all run on the Longleaf CPUs, only `Segment_Images.py` are run on the Longleaf GPUs.

## Set up to run code:
Clone this repository to your home directory on the Longleaf cluster. To run segmentation, you must have access to the GPU partition on Longleaf. If you do not already have access to the Longleaf GPUs, email research@unc.edu to request access.

Within the `.sh` SLURM job submission scripts, there is just one attribute that needs to be modified at setup: your email on the line `#SBATCH --mail-user=` to receive emails when your job runs, finishes running, or fails. Make sure to do this for all of the `.sh` SLURM job submission scripts in this repo. 

## Workflow for a dataset:
### Step 1: Preprocessing

The first step for image segmentation will be to ensure the images are in the proper format for segmentation. Log into Longleaf and navigate to the directory where this cloned repo is located.

First, the movies must be in the form of an image sequence rather than a tiff stack. If the movies are in the form of a tiff stack, then `Unstack_TiffStacks.py` must be run, which is done by submitting the SLURM job submission script `unstack_submitjob.sh`. There are two attributes that must be changed in this job submission script: the first and second arguments after `python ./Unstack_TiffStacks.py`. The first argument should be the path to the folder where the tiff stacks to unstack are located and the second argument should be the name of the folder you wish to create to save the unstacked images to. Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch unstack_submitjob.sh
``` 
*CAUTION: Currently the code creates this folder to save the unstacked images in the directory `/proj/telston_lab/projects/data/reformatted` by default. This means you must have access to the `/proj/telston_lab/` directory before running `Unstack_TiffStacks.py`. This may change in the future to allow for greater utility by also specifying the path where to save the unstacked images, but this is not yet implemented.* If the movies are already in the form of an image sequence, you may skip this step and proceed to the next step in the preprocessing section.

The next step in preprocessing is to generate a histogram of intensities of all the images in a directory that is to be analyzed. Before proceeding, make sure your movies are in the form of an image sequence and not a tiff stack. To generate the histogram of intensities, `GenerateIntensityHistogram.py` is run with the `intensityhist_submitjob.sh` SLURM job submission script. There are two attributes that need to be changed in this job submission script: the first and second arguments after `python ./GenerateIntensityHistogram.py`. The first argument should be the path to the folder where the movies in the form of an image sequence are located to generate the intensity histogram from and the second argument should be the path where you would like to save the histogram of intensities to. Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch intensityhist_submitjob.sh
```

The last step in preprocessing is to rescale the image intensities, ensuring the images are 8 bit and in RGB format, and making sure the images are square and padding with zeros if not. To perform the final preprocessing step, run `PreprocessImages.py `, which is done by submitting the `preprocessingimages_submitjob.sh` SLURM job submission script. There are three attributes which must be changed in this job submission script: the last three arguments after `python ./PreprocessImages.py`. The first of these arguments is the path of the images you wish to preprocess (in the form of an image sequence and not a tiff stack). The last two arguments are the minimum and maximum intensity values to rescale the images to, respectively. These min and max values are obtained from the intensity histogram generated in the previous preprocessing step. The min and max values should capture the minimum and maximum values in the histogram (from x-axis). Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch preprocessingimages_submitjob.sh
```
The output of this script is that images are resaved in the appropriate format in the same location from which they were located originally (CAUTION: the original images will be rewritten).

### Step2: Segmentation

Once you have the preprocessed images, they are now ready for segmentation. To segment, there is only 1 attribute that needs to be changed in both `membrane_submitjob.sh` and `nucleus_submitjob.sh`: the first argument after `python ./Segment_Images.py`, which is the path to the images. Simply change this path to the appropriate path of where the preprocessed images you wish to segment are located. *Note: the first argument is the path to the directory where the DIC images are located, the second argument is the path to the saved keras model to apply in the `keras_unet_models` folder, the third argument is the feature of interest to segment.* To segment the cell membrane, simply type: 

```
sbatch membrane_submitjob.sh
``` 

into the command line (make sure once again you are in the directory of this cloned repo for this command to work). Similarly, to segment cell nucleus, type:

```
sbatch nucleus_submitjob.sh
```

 You can segment both membrane and nucleus at the same time by entering the commands back to back.



