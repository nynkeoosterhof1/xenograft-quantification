
from file_manager import FileManager
from single_channel_preprocessor import SingleChannelPreprocessor
import os
import numpy as np
from skimage.io import imread, imsave
from skimage.util import img_as_uint


class SamplePreprocessor(FileManager):

    def __init__(self, path_folder, channels_to_preprocess=['Gray']):
        super().__init__(path_folder)
        self.folder_path = path_folder
        self.subfolders = self.get_subfolders(self.folder_path)
        self.channels_to_preprocess = self.get_channels_to_preprocess(channels_to_preprocess)
        self.common_files = self.get_common_files_in_subfolders()

    def get_channels_to_preprocess(self, channels_to_preprocess):
        channels = []
        for channel in channels_to_preprocess:
            channels.append(channel + '/')
        return channels
 
    def get_common_files_in_subfolders(self):
        file_lists = []
        for subfolder in self.subfolders:
            file_lists.append(os.listdir(subfolder))
        return list(set.intersection(*[set(list) for list in file_lists]))
    

    def preprocess_sample(self, preprocessing_steps=['clahe_per_slice', 'median'], clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
        for channel in self.channels_to_preprocess:
            preprocessor = SingleChannelPreprocessor(self.folder_path + channel)
            preprocessor.preprocess_images(preprocessing_steps=preprocessing_steps, clipLimit=clipLimit, nbins=nbins, footprint=footprint)
