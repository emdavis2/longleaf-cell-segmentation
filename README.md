Cell Segmentation on UNC Longleaf Cluster
================
## Quick Summary:
This repo contains code to perform binary mask generation of DIC images of JR20 dermal fibroblast cells through the use of a CNN run using a GPU. Specifically, this repo contains instructions for running the code on the UNC Longleaf cluster. Here is a quick overview of the files in this repo and what they do:

`Unstack_TiffStacks.py` is a python script that takes a folder of movies that are in tiff stack form and saves them as image sequences instead. The "unstacked" images are saved in a folder called "reformatted" located at the following path `/proj/telston_lab/projects/data/reformatted`. `unstack_submitjob.sh` is a SLURM job submission script to run `Unstack_TiffStacks.py`. Before running, the first and second string in the last line of the SLURM job submission script needs to be changed to denote the location of the folder of tiff stacks and the name of folder to save the unstacked images to in the `/proj/telston_lab/projects/data/reformatted` directory, respectively.

The file `GenerateIntensityHistogram.py` is a python script that makes a histogram of the image intensity values and saves them to a specified folder. This is used as a part of the preprocessing step and used to ensure that the intensities are appropriately rescaled. `intensityhist_submitjob.sh` is a SLURM job submission script to run `GenerateIntensityHistogram.py`. Before running, the first and second string in the last line of the SLURM job submission script needs to be changed to denote the location of the image sequences to generate an intensity histogram from and the path where to save the histogram to, respectively. 

The file `PreprocessImages.py` is a python script that performs the image preprocessing by rescaling the intensities according to the intensity histograms, as well as making sure the images are 8 bit and in RGB format as well as ensuring the dimensions are square (if dimensions are not square, padding with zeros is performed). The preprocessed images overwrite the existing images. `preprocessimages_submitjob.sh` is a SLURM job submission script to run `PreprocessImages.py`. Before running, the string in the last line of the SLURM job submission script must be changed to denote the location of the image sequences to be preprocessed and the last two images of the last line need to be changed to the minimum and maximum values of intensity to rescale the images, respectively. The min and max intensity values should be determined from the intensity histogram generated from `GenerateIntensityHistorgram.py`.

The file `Segment_Images.py` is a python script that uses a CNN model saved with keras to segment the preprocessed DIC images, make a directory where the images are located and saves the masks there. It uses the GPU node on the Longleaf cluster and it takes in five arguments: the path where the preprocessed DIC images to be segmented are located, the movie number to be segmented, the path where the saved keras model architecture is saved (in json file form), the path where the weights to the keras model is saved (in h5 file form), and lastly, the type of mask that is being generated (membrane or nucleus). `membrane_submitjob.sh` is a SLURM job submission script to use the pretrained keras membrane CNN model to segment membrane and `nucleus_submitjob.sh` is a SLURM job submission script to use the pretrained keras nucleus CNN model to segment nucleus. Each of these SLURM job submission scripts requires 2 arguments: the path to where the preprocessed images to be segmented are located and the movie number to segment. These arguments are given in the `submit_all_jobs.sh` file and its purpose is to submit SLURM jobs for each movie for both membrane and nucleus in a loop so multiple jobs can be submitted just by running this file. This file is the only file that needs to be edited to segment images; the only 2 things that need to be changed are the path to the images to segment for the `IMG_PATH` variable in line 3 and the range of movie numbers to segment in line 5. 

A required folder is `keras_unet_models`, as it contains the trained CNN models (saved with keras) which are used to segment the cell membrane and cell nucleus. There are 2 models in this folder with 4 files total: json and h5 files for membrane and json and h5 files for nucleus. Currently this folder is located on the following path: `/proj/telston_lab/projects/keras_unet_models` and the membrane files are located in the `membrane` subdirectory and the nucleus files are located in the `nucleus` subdirectory. *Note: You must have access to the `/proj/telston_lab` space to access this folder.*

Note: `Unstack_TiffStacks.py`, `GenerateIntensityHistogram.py`, and `PreprocessImages.py` are all run on the Longleaf CPUs, only `Segment_Images.py` are run on the Longleaf GPUs.

## Set up to run code:
Clone this repository to your home directory on the Longleaf cluster. To run segmentation, you must have access to the GPU partition on Longleaf. If you do not already have access to the Longleaf GPUs, email research@unc.edu to request access.

Next, you must make 2 files executable: `Segment_Images.py` and `submit_all_jobs.sh`. To do this, you must run the commands:

```
chmod +x Segment_Images.py
```

and 

```
chmod +x submit_all_jobs.sh
```

Now, the code should be ready to run.

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

The last step in preprocessing is to rescale the image intensities, ensuring the images are 8 bit and in RGB format, and making sure the images are square and padding with zeros if not. To perform the final preprocessing step, run `PreprocessImages.py `, which is done by submitting the `preprocessimages_submitjob.sh` SLURM job submission script. There are three attributes which must be changed in this job submission script: the last three arguments after `python ./PreprocessImages.py`. The first of these arguments is the path of the images you wish to preprocess (in the form of an image sequence and not a tiff stack). The last two arguments are the minimum and maximum intensity values to rescale the images to, respectively. These min and max values are obtained from the intensity histogram generated in the previous preprocessing step. The min and max values should capture the minimum and maximum values in the histogram (from x-axis). Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch preprocessimages_submitjob.sh
```
The output of this script is that images are resaved in the appropriate format in the same location from which they were located originally (CAUTION: the original images will be rewritten).

### Step2: Segmentation

Once you have the preprocessed images, they are now ready for segmentation. To segment, there are only 2 attributes that needs to be changed in `submit_all_jobs.sh`: the variable `IMG_PATH`, which is the path to the images, and the smallest and largest movie numbers to segment in `{<min>..<max>}` in line 5. Once that is done, you are ready to segment the cell membrane and nucleus by typing: 

```
./submit_all_jobs.sh
``` 

into the command line. Once the jobs run, the images should be appropriately segmented.