

from file_manager import FileManager
import os
from skimage.filters import median 
import numpy as np
from skimage.util import img_as_ubyte
from skimage.exposure import equalize_adapthist
from skimage.io import imread, imsave

class SingleChannelPreprocessor(FileManager):

    def __init__(self, path_folder):
        super().__init__(path_folder)
        self.folder = path_folder
        self.image_files = os.listdir(self.folder)
        self.preprocessed_folder = self.make_new_folder(self.folder, 'preprocessed')
        self.subfolders = self.get_subfolders(self.folder)
        self.images_to_preprocess = self.get_images_to_preprocess()

    def get_images_to_preprocess(self):
        im = []
        for image in self.image_files:
            if len(image.split('.')) == 2:
                im.append(image)
        return im
    
    def median_filter(self, img, footprint=np.ones((5,5)), behavior='ndimage'):
        med = np.zeros((img.shape))
        for i in range(img.shape[0]):
            med[i,:,:] = median(img[i,:,:], footprint=footprint, behavior=behavior)
        return med

    def make_8bit(self, img, mode='skimage'):
        if mode == 'skimage':
            return img_as_ubyte(img)
        elif mode == 'numpy':
            return img.astype(dtype=np.uint8)

    def clahe_per_slice(self, img, clipLimit=0.07, nbins=127):
        cl = np.zeros((img.shape))
        for i in range(img.shape[0]):
            cl[i,:,:] = equalize_adapthist(img[i,:,:], clip_limit = clipLimit, nbins=nbins)
        return cl

    def clahe_total(self, img, clipLimit=0.07, nbins=127):
        return equalize_adapthist(img, clip_limit = clipLimit, nbins=nbins)
    
    def preprocess_images(self, preprocessing_steps=['clahe_per_slice', 'median'], clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
        for image in self.images_to_preprocess:
            img = imread(self.folder + image)
            img = self.make_8bit(img)
            if 'clahe_per_slice' in preprocessing_steps:
                img = self.clahe_per_slice(img, clipLimit=clipLimit, nbins=nbins)
            elif 'clahe_total' in preprocessing_steps:
                img = self.clahe_total(img, clipLimit=clipLimit, nbins=nbins)
            img = self.make_8bit(img)
            if 'median' in preprocessing_steps:
                img = self.median_filter(img, footprint=footprint)
                img = self.make_8bit(img, mode='numpy')
            imsave(self.preprocessed_folder + image, img)