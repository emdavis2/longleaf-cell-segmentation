from skimage.io import imread, imsave, imshow
import os
import numpy as np
import ntpath
import matplotlib.pyplot as plt
import sys
import ntpath

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files
image_path = str(sys.argv[1])

fig_savepath = str(sys.argv[2])
####################################

#lists all the files that are within imagesfolder and stores them in a variable called "imagenames"
imagenames=os.listdir(image_path)
#filter out filenames that are not .tif files
imagenames = list(filter(lambda file: file[-4:] == '.tif', imagenames))
#sort filenames numerically
imagenames.sort()

#plot histogram of image intensities 
for i in range(len(imagenames)):
  if imagenames[i].endswith('.tif'):
    image=imread(image_path + '/' +imagenames[i])
    plt.hist(image.ravel(),50)
plt.xlim(0,25000)
plt.savefig(fig_savepath + '/{}_IntensityHist.png'.format(ntpath.basename(image_path)))