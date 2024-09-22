
from file_manager import FileManager
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imsave
from skimage.measure import regionprops
from skimage.util import img_as_uint, img_as_ubyte
import pandas as pd
import glob
import os



class CellCounter(FileManager):

    def __init__(self, path_folder, image_name, labelmap_2D, labelmap_3D, threshold_ratio = 0.8, threshold_size = 300):
        super().__init__(path_folder)
        self.labelmap_2D = labelmap_2D
        self.labelmap_3D = labelmap_3D 
        self.threshold_ratio = threshold_ratio
        self.threshold_size = threshold_size
        self.image_name = image_name
        self.result = {'labels_total': [], 'total_count': 0,} 

    def make_binary(self, mask):
        bin_mask = np.zeros(mask.shape)
        bin_mask[mask > 0] = 1
        return bin_mask     

    def apply_mask(self, labelmap, mask):
        return labelmap * mask
    
        
    def get_regionProps(self, labelmap):
        return regionprops(labelmap.astype(dtype=np.uint16))
    
    def get_total_labels(self):
        labels = [] 
        bin_nuclear_mask = self.make_binary(self.labelmap_2D) 
        self.labelmap_3D = self.apply_mask(self.labelmap_3D, bin_nuclear_mask)
        properties_3D_labelmap = self.get_regionProps(self.labelmap_3D) 

        for prop in properties_3D_labelmap:
            labels.append(prop['label']) 
        
        self.result['labels_total'] = labels
        self.make_new_folder(self.folder, 'labels_total')
        imsave(self.folder + 'labels_total/' + self.image_name, self.labelmap_3D.astype(dtype=np.uint16))

    def get_results(self):
        self.get_total_labels()
        self.result['total_count'] = len(self.result['labels_total'])
        return self.result

