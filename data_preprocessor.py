
from msilib.schema import File
from file_manager import FileManager
from sample_preprocessor import SamplePreprocessor
import numpy as np

class DataPreprocessor(FileManager):

    def __init__(self, path_folder, channels_to_preprocess = ['Gray']):
        super().__init__(path_folder)
        self.folder_path = path_folder
        self.sample_folders = self.get_subfolders(self.folder_path)
        self.channels_to_preprocess = channels_to_preprocess

    def preprocess_images(self, preprocessing_steps=['clahe_per_slice', 'median'], clipLimit=0.07, nbins=127, footprint=np.ones((5,5))):
        for sample_folder in self.sample_folders:
            sample_preprocessor = SamplePreprocessor(sample_folder, self.channels_to_preprocess)
            sample_preprocessor.preprocess_sample(preprocessing_steps=preprocessing_steps, clipLimit=clipLimit, nbins=nbins, footprint=footprint)


