#Import libraries

from skimage.io import imread, imsave
import os
import numpy as np
import ntpath
import sys

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files

#path where tiff stacks are located
movies_path = str(sys.argv[1])

#path to folder and name of folder to store unstacked tiff images (folder doesn't have to exist, it will be created if it does not exist yet)
reformat_folder_path = str(sys.argv[2])

#whether there are bead images for traction force microscopy or not (input expected is 1 or 0, where 1 means True and 0 means False)
is_beads = bool(sys.argv[3])
####################################

#make directory to store unstacked movies
if not os.path.exists(reformat_folder_path):
    os.mkdir(reformat_folder_path)

#make directory to store unstacked movies - makes it in a folder called "reformatted" in the /proj/telston_lab/projects/data directory
if is_beads:
    bead_folder_path = reformat_folder_path + '/beads'
    if not os.path.exists(bead_folder_path):
        os.mkdir(bead_folder_path)

#get name of all tiff stacks in movies_path folder
movie_names=os.listdir(movies_path)
#filter out filenames that are not .tif files
movie_names = list(filter(lambda file: file[-4:] == '.tif', movie_names))
#sort filenames numerically
movie_names.sort()

#loop through tiff stacks and save individual frames in specified saving path 
for mov_num, movie in enumerate(movie_names):
    mov = imread(movies_path + '/' + movie)
    #if len of movie dimension is > 3 that means there is an extra channel with the bead images, so separate and save appropriately
    #currently this code assumes the first channel is beads and second is DIC - may need to change in future
    if len(np.shape(mov)) > 3:
        for frame in range(1,np.shape(mov)[0]+1):
            imsave(reformat_folder_path + '/' + ntpath.basename(reformat_folder_path) +'_s{}_t{}.tif'.format(mov_num+1, frame), mov[frame-1][1],check_contrast=False)
            imsave(bead_folder_path + '/' + ntpath.basename(reformat_folder_path) +'_s{}_t{}.tif'.format(mov_num+1, frame), mov[frame-1][0],check_contrast=False)
    else:
        for frame in range(1,np.shape(mov)[0]+1):
            imsave(reformat_folder_path + '/' + ntpath.basename(reformat_folder_path) +'_s{}_t{}.tif'.format(mov_num+1, frame), mov[frame-1],check_contrast=False)