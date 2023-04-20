#Import libraries

import os
import sys
import numpy as np
import ntpath

from tensorflow.keras.preprocessing.image import load_img
from tensorflow import keras
from tensorflow.keras import optimizers

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files

#path where preprocessed images are located to be segmented
input_dir = str(sys.argv[1])

#path where keras model is saved
model_save_path = str(sys.argv[2])

#path where to save segmented images 
mask_type = str(sys.argv[3])
####################################


#call our trained model "loaded_model" and load it 
loaded_model = keras.models.load_model(model_save_path)


#lists all the files that are within imagesfolder and stores them in a variable called "imagenames"
imagenames=os.listdir(input_dir)



#list of paths to the images to be segmented
input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
        if fname.endswith(".tif")
    ]
)


print("Number of samples:", len(input_img_paths)) #number of images that will be segmented



#define a class to feed the data in to the model (taken from here: https://keras.io/examples/vision/oxford_pets_image_segmentation/)
class CellSegmenter(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths

    def __len__(self):
        return len(self.input_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        return x, y




#size to resize the images to
img_size = (1024, 1024)
#number of classifications (1=cell or nuclues [depending on what you are segmenting], 0=background)
num_classes = 2
#number of images to feed in at a time
batch_size = 1



#get data into the format needed to feed into the CNN ("val_gen")
#get the binary masks for the images ("val_preds")
val_gen = CellSegmenter(batch_size, img_size, input_img_paths[:])
val_preds = loaded_model.predict(val_gen)


#make directory to store masks
mask_folder_path = input_dir + '/' + mask_type + '_masks'
os.mkdir(mask_folder_path)


#save masks to folder
for i in range(len(val_preds)):
  mask = np.argmax(val_preds[i], axis=-1)
  mask = np.expand_dims(mask, axis=-1)
  img = keras.preprocessing.image.array_to_img(mask)
  img.save(mask_folder_path+'/'+ntpath.basename(input_img_paths[i][:-3])+'TIF')
