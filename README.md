Cell Segmentation on UNC Longleaf Cluster
================
## Quick Summary of Repo Contents:
This repo contains code to perform binary mask generation of DIC images of JR20 dermal fibroblast cells through the use of a CNN run using a GPU. The code is also formatted to work with data that contains images of fluorescently labeled beads used for traction force microscopy in addition to just DIC images. Specifically, this repo contains instructions for running the code on the UNC Longleaf cluster. Here is a quick overview of the files in this repo and what they do:

`Unstack_TiffStacks.py` is a python script that takes a folder of movies that are in tiff stack form and saves them as image sequences instead. `unstack_submitjob.sh` is a SLURM job submission script to run `Unstack_TiffStacks.py`. Before running, the first, second, and third strings in the last line of the SLURM job submission script needs to be changed to denote the location of the folder of tiff stacks, and entire path to the folder to save the unstacked images to, and whether the image stacks contain a channel of fluorescent beads used for traction force microscopy.

However, if the movies to be segmented are saved as an image sequence instead of a tiff stack, `Move_Rename.py` is a python script that renames the images in the proper naming convention and saves them in a new location. As a note, this script is not stable nor entirely generalizable at the moment since it has some aspects, such as movie type (substrate that cell is imaged on) depending on movie number that is hard-coded in. In a future release, this will be fixed to be more general. `moverename_submitjob.sh` is a SLURM job submission script to run `Move_Rename.py`. In this job submission script, the first and second and third strings in the last line of the script needs to be changed to denote: 1. the path of the folder of the data that needs to be renamed is located and the location 2. the path of where to save the renamed images to 3. the name of the folder that will be created in the image save location (2.).

Note: only one (`Unstack_TiffStacks.py` or `Move_Rename.py`) needs to be run. This depends on the format of your data. If your data is a tiff stack, use `Unstack_TiffStacks.py`. Else, if your data is in image sequence format (individual tiff images), use `Move_Rename.py`.

The file `GenerateIntensityHistogram.py` is a python script that makes a histogram of the image intensity values and saves them to a specified folder. This is used as a part of the preprocessing step and used to ensure that the intensities are appropriately rescaled. `intensityhist_submitjob.sh` is a SLURM job submission script to run `GenerateIntensityHistogram.py`. Before running, the first and second string in the last line of the SLURM job submission script needs to be changed to denote the location of the image sequences to generate an intensity histogram from and the path where to save the histogram to, respectively. 

The file `PreprocessImages.py` is a python script that performs the image preprocessing by rescaling the intensities according to the intensity histograms, as well as making sure the images are 8 bit and in RGB format as well as ensuring the dimensions are square (if dimensions are not square, padding with zeros is performed). The preprocessed images overwrite the existing images. `preprocessimages_submitjob.sh` is a SLURM job submission script to run `PreprocessImages.py`. Before running, the string in the last line of the SLURM job submission script must be changed to denote the location of the image sequences to be preprocessed and the last two images of the last line need to be changed to the minimum and maximum values of intensity to rescale the images, respectively. The min and max intensity values should be determined from the intensity histogram generated from `GenerateIntensityHistorgram.py`.

The file `Segment_Images.py` is a python script that uses a CNN model saved with keras to segment the preprocessed DIC images, make a directory where the images are located and saves the masks there. It uses the GPU node on the Longleaf cluster and it takes in five arguments: the path where the preprocessed DIC images to be segmented are located, the movie number to be segmented, the path where the saved keras model architecture is saved (in json file form), the path where the weights to the keras model is saved (in h5 file form), and lastly, the type of mask that is being generated (membrane or nucleus). `membrane_submitjob.sh` is a SLURM job submission script to use the pretrained keras membrane CNN model to segment membrane and `nucleus_submitjob.sh` is a SLURM job submission script to use the pretrained keras nucleus CNN model to segment nucleus. Each of these SLURM job submission scripts requires 2 arguments: the path to where the preprocessed images to be segmented are located and the movie number to segment. These arguments are given in the `submit_all_jobs.sh` file and its purpose is to submit SLURM jobs for each movie for both membrane and nucleus in a loop so multiple jobs can be submitted just by running this file. This file is the only file that needs to be edited to segment images; the only 2 things that need to be changed are the path to the images to segment for the `IMG_PATH` variable in line 3 and the range of movie numbers to segment in line 5. 

A required folder is `keras_unet_models`, as it contains the trained CNN models (saved with keras) which are used to segment the cell membrane and cell nucleus. There are 2 models in this folder with 4 files total: json and h5 files for membrane and json and h5 files for nucleus. Currently this folder is located on the following path: `/proj/telston_lab/projects/keras_unet_models` and the membrane files are located in the `membrane` subdirectory and the nucleus files are located in the `nucleus` subdirectory. *Note: You must have access to the `/proj/telston_lab` space to access this folder.*

Note: `Unstack_TiffStacks.py`, `GenerateIntensityHistogram.py`, and `PreprocessImages.py` are all run on the Longleaf CPUs, only `Segment_Images.py` is run on the Longleaf GPUs.

## Set up to run code:
Clone this repository to your home directory on the Longleaf cluster. To run segmentation, you must have access to the GPU partition on Longleaf. If you do not already have access to the Longleaf GPUs, email research@unc.edu to request access. Additionally, make sure you are running python through Anaconda. To check which installation of python is being used, type `which python` into the terminal when logged into Longleaf. The output should be `~/anaconda3/bin/python`. If that is not the case, type `module add anaconda`. To save so that the Anaconda is automatically loaded each time you log into the system, type `module save`. Type `module list` to see a list of loaded in modules and confirm that Anaconda has been added.

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

First, the movies must be in the form of an image sequence rather than a tiff stack. If the movies are in the form of a tiff stack, then `Unstack_TiffStacks.py` must be run, which is done by submitting the SLURM job submission script `unstack_submitjob.sh`. There are three attributes that must be changed in this job submission script: the first, second, and third arguments after `python ./Unstack_TiffStacks.py`. The first argument should be the path to the folder where the tiff stacks to unstack are located, the second argument should be the path to the folder you wish to save the unstacked images to (note: this folder does not have to exist, it will be created if it does not), and lastly the third argument should be a 0 (False) or 1 (True) depending on whether your images have a channel for fluorescent beads or not. Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch unstack_submitjob.sh
``` 
If the movies are already in the form of an image sequence AND in the proper naming convention ({*descriptive_name*}_s{*movie_number*}_t{*frame_number*}.tif), you may skip this step and proceed to the next step in the preprocessing section (`GenerateIntensityHistogram.py`). Otherwise, if the data is in the form of an image sequence but NOT in the right naming convention, `Move_Rename.py` needs to be run. This is done by submitting the SLURM job submission script `moverename_submitjob.sh`. There are three attributes that need to be changed in this job submission script: the first, second, and third arguments after `python ./Move_Rename.py`. The first argument should be the path to the folder where the tiff images to be renamed are located. The second argument is the path to the directory where a folder will be created to move the renamed images to. The third argument is the name of the folder to be created to save renamed images to. Once the necessary changes are made, run the script on Longleaf by typing:
```
sbatch moverename_submitjob.sh
```

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