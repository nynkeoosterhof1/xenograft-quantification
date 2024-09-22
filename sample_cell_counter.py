
from msilib.schema import File
from cell_counter import CellCounter
from file_manager import FileManager
from skimage.io import imread, imsave
from skimage.util import img_as_uint, img_as_ubyte
from skimage.segmentation import mark_boundaries
import os
import numpy as np
import pandas as pd
import json

class SampleCellCounter(FileManager):

    def __init__(self, path_folder, labelmaps_2D, labelmaps_3D, threshold_ratio=0.8, threshold_size=300):
        super().__init__(path_folder)
        self.folder_labelmaps_2D = self.folder + labelmaps_2D + '/'
        self.folder_labelmaps_3D = self.folder + labelmaps_3D + '/'
        self.threshold_ratio = threshold_ratio
        self.threshold_size = threshold_size
        self.files = os.listdir(self.folder_labelmaps_2D)
        self.results = {}

    def get_results(self):
        for file in self.files:
            labelmap_2D = imread(self.folder_labelmaps_2D + file)
            labelmap_3D = imread(self.folder_labelmaps_3D + file)

            counter = CellCounter(self.folder, file, labelmap_2D, labelmap_3D, self.threshold_ratio, self.threshold_size)
            self.results[file] = counter.get_results()
        return self.results
  
    def generate_labelmap_from_labels(self, labels, template_labelmap):
        new_labelmap = np.zeros(template_labelmap.shape)
        for label in labels:
            new_labelmap[template_labelmap == label] = label
        return new_labelmap.astype(dtype=np.uint16)
    
    def save_labelmaps(self, new_folders=['labels_total', 'labels_human_nuclei']):
           for file in self.files:
            labelmap_3D = imread(self.folder_labelmaps_3D + file)
            
            for folder in new_folders:
                labelmap_folder = self.make_new_folder(self.folder, folder)
                new_labelmap = self.generate_labelmap_from_labels(self.results[file][folder], labelmap_3D)
                imsave(labelmap_folder + file, new_labelmap)
    
    def make_composites(self, new_folder_name, mode):
        new_folder_path = self.make_new_folder(self.folder, new_folder_name)
        if mode == 'nuclei':
            folder_orig = self.folder + 'Cyan/'
            folder_labels = self.folder + 'labels_total/'
        else:
            pass

        for file in self.files:
            original_img = imread(folder_orig + file)
            label_img = imread(folder_labels + file)
            combined = self.get_outlines(original_img, label_img)
            imsave(new_folder_path + file, combined)

    def get_outlines(self, original_img, label_img):
        outline_image = np.zeros((original_img.shape[0], original_img.shape[1], original_img.shape[2], 3))
        for i in range(outline_image.shape[0]):
            outline_image[i,:,:,:] = mark_boundaries(original_img[i,:,:], label_img[i,:,:])
        return img_as_ubyte(outline_image[:,:,:,0])
    
    
    def make_data_summary(self):
        self.data_summary = {}
        for sample, data in self.results.items():
            summary = {}
            for key, value in data.items():
                if key != 'labels_total':
                    summary[key] = value
            self.data_summary[sample] = summary
        return self.data_summary

    def save_results(self):

        with open(self.folder + 'results.json', mode='w') as f:
            json.dump(self.results, f)
        
        with open(self.folder + 'result_summary.json', mode='w') as f:
            json.dump(self.data_summary, f)
        
        df = pd.DataFrame(self.data_summary).T
        df.to_excel(self.folder + 'results.xlsx')  


    def analyze_sample(self):
        self.get_results()
        self.make_composites('segmentation_nuclei', mode='nuclei')
        self.make_data_summary()
        self.save_results()        


