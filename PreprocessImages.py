import imageio
from skimage.io import imread, imsave, imshow
from skimage.exposure import rescale_intensity
from skimage import exposure
import os
import numpy as np
from pathlib import Path
import re
import ntpath
import sys
import random
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageOps
import PIL

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files
image_path = str(sys.argv[1])

#Minimum and maximum intensity values taken from historgrams from GenerateIntensityHistorgram.py 
min_val = int(sys.argv[2])
max_val = int(sys.argv[3])
####################################

#lists all the files that are within imagesfolder and stores them in a variable called "imagenames"
imagenames=os.listdir(image_path)
#filter out filenames that are not .tif files
imagenames = list(filter(lambda file: file[-4:] == '.tif', imagenames))
#sort filenames numerically
imagenames.sort()

#function that pads an array to make it a sqaure
#note: if the array is already a square it doesn't pad
def pad_with_zeros_to_square_applymodel(img):
  x_dim = np.shape(img)[0]
  y_dim = np.shape(img)[1]

  diff = x_dim - y_dim
  
  if diff < 0:
    pad_img = np.pad(img, ((0, np.abs(diff)),(0,0),(0,0)),'constant', constant_values=0)
  if diff > 0:
    pad_img = np.pad(img, ((0, 0),(0,np.abs(diff)),(0,0)),'constant', constant_values=0)
  elif diff == 0:
    pad_img = img
  return pad_img

#get images, rescale intensity, put them in 8 bit and rgb, and pad images to make them a square and save 
for imagename in imagenames:
  #rescale intensity for each image
  bright = rescale_intensity(imread(image_path + '/' + imagename),(min_val,max_val))
  #convert to 8 bit from 16 bit
  bright8b= (bright/256).astype('uint8')
  #convert gray to rgb
  brigth8b_rgb=np.stack((bright8b,bright8b,bright8b),axis=2)
  image = pad_with_zeros_to_square_applymodel(brigth8b_rgb)
  imsave(image_path + '/' + imagename, image)