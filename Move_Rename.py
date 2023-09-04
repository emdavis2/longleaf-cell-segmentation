import os
import numpy as np
import ntpath
import sys
import shutil

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files

#path where images are located to renamed and moved to a different location
input_dir = str(sys.argv[1])

#path to base directory of save location where renamed images will be moved to 
save_path = str(sys.argv[2])

#folder base name - the basename of the directory where the images will be moved to 
folder_basename = str(sys.argv[3])
####################################


#lists all the files that are within imagesfolder and stores them in a variable called "imagenames"
imagenames=os.listdir(input_dir)
#filter out filenames that are not .tif files
imagenames = list(filter(lambda file: file[-4:] == '.tif', imagenames))
#sort filenames numerically
imagenames.sort()

glass_savepath = save_path+'/'+folder_basename+'_glass'
stiff_savepath = save_path+'/'+folder_basename+'_stiff'
soft_savepath = save_path+'/'+folder_basename+'_soft'

glass_mov = np.arange(1,37)
soft_mov = np.arange(37,73)
stiff_mov = np.arange(73,109)

#check to see if the path exists, if not make the directory of folder to move images to
if not os.path.exists(glass_savepath):
  os.mkdir(glass_savepath)
#check to see if the path exists, if not make the directory within the folder where images are being moved to for the bead images
if not os.path.exists(glass_savepath+'/beads'):
  os.mkdir(glass_savepath+'/beads')

  #check to see if the path exists, if not make the directory of folder to move images to
if not os.path.exists(soft_savepath):
  os.mkdir(soft_savepath)
#check to see if the path exists, if not make the directory within the folder where images are being moved to for the bead images
if not os.path.exists(soft_savepath+'/beads'):
  os.mkdir(soft_savepath+'/beads')

#check to see if the path exists, if not make the directory of folder to move images to
if not os.path.exists(stiff_savepath):
  os.mkdir(stiff_savepath)
#check to see if the path exists, if not make the directory within the folder where images are being moved to for the bead images
if not os.path.exists(stiff_savepath+'/beads'):
  os.mkdir(stiff_savepath+'/beads')



for file in imagenames:
  movie_num = int(file[6:9])
  frame_num = int(file[1:4])
  channel = file[9:11]
  file_end = 's{}_t{}.tif'.format(movie_num, frame_num)
  if movie_num in glass_mov:
    if channel == 'c2':
      shutil.copy2(os.path.join(input_dir, file), glass_savepath+'/'+folder_basename+'_glass_'+file_end)
    elif channel == 'c1':
      shutil.copy2(os.path.join(input_dir, file), glass_savepath+'/beads/'+folder_basename+'_beads_glass_'+file_end)

  elif movie_num in soft_mov:
    if channel == 'c2':
      shutil.copy2(os.path.join(input_dir, file), soft_savepath+'/'+folder_basename+'_soft_'+file_end)
    elif channel == 'c1':
      shutil.copy2(os.path.join(input_dir, file), soft_savepath+'/beads/'+folder_basename+'_beads_soft_'+file_end)

  elif movie_num in stiff_mov:
    if channel == 'c2':
      shutil.copy2(os.path.join(input_dir, file), stiff_savepath+'/'+folder_basename+'_stiff_'+file_end)
    elif channel == 'c1':
      shutil.copy2(os.path.join(input_dir, file), stiff_savepath+'/beads/'+folder_basename+'_beads_stiff_'+file_end)