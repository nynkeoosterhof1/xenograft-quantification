
## The top part of the scripts contains the code to set variables, while the lower part contains the code to do the operations,
## which means the code it not run from top to bottom but rather per operation. To make sure everythin is run in the right order, follow the protocol##
## in general, light green values and orange names/definitoins can be changed ##


######################## Import modules ###############################

import numpy as np
from skimage.io import imread, imsave
import numpy as np
from skimage.measure import regionprops
import os

from image_unpacker import ImageUnpacker
from data_preprocessor import DataPreprocessor
from data_cell_counter import DataCellCounter
from data_intensity_counter import DataIntensityCounter


"""
1. Set Variables
"""

###############  Set path variables  ###########################
RAW_DATA_FOLDER = 'C:/Users/Documents/cellpose_test/'

## do this step to tell computer where to find and store data ##
PATH_LABELMAPS = 'C:/Users/Documents/cellpose_test/experiment_xyz/labelmaps_3D/'
PATH_INTENSITY_IMAGES = 'C:/Users/Documents/cellpose_test/experiment_xyz/Magenta/'
PATH_RESULTS = 'C:/Users/Documents/cellpose_test/experiment_xyz/Results/'

NAME_FOLDER_2D_LABELMAPS = 'labelmaps_2D'
NAME_FOLDER_3D_LABELMAPS = 'labelmaps_3D'

##############  Set preprocessing variables ############################

CHANNELS_TO_PREPROCESS = ['Cyan'] 

## adjust preprocessing parameters below ##

PREPROCESSING_STEPS = ['clahe_per_slice', 'median'] #options: clahe_per_slice , clahe_total, median
CLIP_LIMIT = 0.05 # For clahe histogram equalization
NBINS = 127 # For clahe histogram equalization
FOOTPRINT = np.ones((5,5)) # For median filter


################ Data analysis settings (intensity) #############

NAME_RESULTS_FILE = 'results.json'
NAME_LABELMAP_FOLDER = 'labels_total'
CHANNELS_TO_USE = ['Yellow']
MODE = 'max'     #Options are 'mean' or 'max' or 'mean/max'
CHANNEL_THRESHOLDS_MEAN = [30] ## two values are needed if two channels are used ##
CHANNEL_THRESHOLDS_MAX = [100]
PREPROCESSED = True


"""
2. Do operations
"""

################# Unpack images #################################

## unzipping of lif files, makes individual channel tif files##

unpack = ImageUnpacker(RAW_DATA_FOLDER)
unpack.unpack_images()


################ Preprocess images ##############################
data_preprocessor = DataPreprocessor(RAW_DATA_FOLDER, CHANNELS_TO_PREPROCESS) 
data_preprocessor.preprocess_images(preprocessing_steps=PREPROCESSING_STEPS, clipLimit=CLIP_LIMIT, nbins=NBINS, footprint=FOOTPRINT)


################### Cellpose ####################################


from cellpose import models
from cellpose import utils
from cellpose import plot
from skimage.util import img_as_uint


PATH_DATA = 'C:/Users/Documents/cellpose_test/experiment_xyz/Cyan/preprocessed/'
PATH_RESULTS_2D = 'C:/Users/Documents/cellpose_test/experiment_xyz/labelmaps_2D/'
PATH_RESULTS_3D = 'C:/Users/Documents/cellpose_test/experiment_xyz/labelmaps_3D/'


image_files = os.listdir(PATH_DATA) 

model = models.Cellpose(gpu=False, model_type='nuclei')
channels = [0,0]


for file in image_files:
  img = imread(PATH_DATA + file) 
  masks, flows, styles, diams = model.eval(img, diameter=25, flow_threshold=0.9, cellprob_threshold=-6, channels=channels, z_axis=0, do_3D=False, stitch_threshold=0.68)
  labelmap_3D = img_as_uint(masks)
  imsave(PATH_RESULTS_3D + file, labelmap_3D)
  masks, flows, styles, diams = model.eval(img, diameter=25, flow_threshold=0.9, cellprob_threshold=-6, channels=channels, z_axis=0, do_3D=False)
  labelmap_2D = img_as_uint(masks)
  imsave(PATH_RESULTS_2D + file, labelmap_2D)



################### Count cells #################################

counter = DataCellCounter(RAW_DATA_FOLDER,NAME_FOLDER_2D_LABELMAPS, NAME_FOLDER_3D_LABELMAPS)
counter.analyze_data()


################### Intensity Counter ##########################

intensity_counter = DataIntensityCounter(RAW_DATA_FOLDER, NAME_RESULTS_FILE, NAME_LABELMAP_FOLDER, CHANNELS_TO_USE, MODE, CHANNEL_THRESHOLDS_MEAN, CHANNEL_THRESHOLDS_MAX, PREPROCESSED)
intensity_counter.count_cells()
intensity_counter.save_results()

