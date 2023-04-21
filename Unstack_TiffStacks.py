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

#name of folder to store unstacked tiff images
folder_name = str(sys.argv[2])
####################################

#make directory to store unstacked movies
reformat_folder_path = '/proj/telston_lab/projects/data/reformatted/' + folder_name
os.mkdir(reformat_folder_path)

#get name of all tiff stacks in movies_path folder and sort them numerically
movie_names=os.listdir(movies_path)
movie_names.sort()

#loop through tiff stacks and save individual frames in specified saving path 
for mov_num, movie in enumerate(movie_names[0:2]):
    mov = imread(movies_path + '/' + movie)
    for frame in range(1,np.shape(mov)[0]+1):
        imsave(reformat_folder_path + '/' + ntpath.basename(reformat_folder_path) +'_s{}_t{}.tif'.format(mov_num, frame), mov[frame-1],check_contrast=False)