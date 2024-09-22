

from cellpose import models
from cellpose import utils
from cellpose import plot
from skimage.io import imsave, imread
from skimage.util import img_as_uint
import os


PATH_DATA = 'C:/Users/Documents/cellpose_test/experiment_xyz/Cyan/'
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
