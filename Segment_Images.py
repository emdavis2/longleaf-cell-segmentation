from tensorflow import keras
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import load_img
import os
import numpy as np
import ntpath
import sys

####################################
#Arguments taken from command line when running this script which can be found in the corresponding .sh files

#path where preprocessed images are located to be segmented
input_dir = str(sys.argv[1])

#movie number to segment from input_dir
movie_num = str(sys.argv[2])

#path to saved keras model
model_save_path_json = str(sys.argv[3])

model_save_path_weights = str(sys.argv[4])

#path where to save segmented images 
mask_type = str(sys.argv[5])
####################################

with open(model_save_path_json) as json_file:
  json_config = json_file.read()
loaded_model = keras.models.model_from_json(json_config)

# Load weights
loaded_model.load_weights(model_save_path_weights)



#lists all the files that are within imagesfolder and stores them in a variable called "imagenames"
imagenames=os.listdir(input_dir)
#filter out filenames that are not .tif files
imagenames = list(filter(lambda file: file[-4:] == '.tif', imagenames))
#filter out movies that do not contain the movie_num from argument input
imagenames = list(filter(lambda file: '_s{}_'.format(movie_num) in file, imagenames))
#sort filenames numerically
imagenames.sort()



#list of paths to the images to be segmented
input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in imagenames 
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
if not os.path.exists(mask_folder_path):
    os.mkdir(mask_folder_path)


#save masks to folder
for i in range(len(val_preds)):
  mask = np.argmax(val_preds[i], axis=-1)
  mask = np.expand_dims(mask, axis=-1)
  img = keras.preprocessing.image.array_to_img(mask)
  img.save(mask_folder_path+'/'+ntpath.basename(input_img_paths[i][:-3])+'TIF')