
from msilib.schema import File
from file_manager import FileManager
import json
from skimage.measure import regionprops
import os
from intensity_counter import IntensityCounter
from skimage.io import imread, imsave
import pandas as pd
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_ubyte
import numpy as np

class SampleIntensityCounter(FileManager):

    def __init__(self, path_folder, results_file, labelmap_folder, channels_to_use, mode = 'mean', channel_thresholds_mean = [], channel_thresholds_max=[], preprocessed=True):
        super().__init__(path_folder)
        self.results = self.open_json(results_file)
        self.channels_to_use = channels_to_use
        self.labelmap_folder = labelmap_folder
        self.files = [f for f in os.listdir(self.folder + self.labelmap_folder) if len(f.split('.')) == 2]
        self.preprocessed = preprocessed 
        self.thresholds_mean = channel_thresholds_mean
        self.thresholds_max = channel_thresholds_max
        self.mode = mode
        self.segmentation_folders = self.make_segmentation_folders()
        self.summary = {}


    def make_segmentation_folders(self):
        segmentation_folders = []
        for channel in self.channels_to_use:
            segmentation_folders.append(self.make_new_folder(self.folder, f'segmentation_human_nuclei'))
        return segmentation_folders
    
    
    def count_cells(self):
        for i in range(len(self.channels_to_use)):
            if self.preprocessed:
                channel_to_count = self.channels_to_use[i] + '/preprocessed/'
            else:
                channel_to_count = self.channels_to_use[i] + '/'
            for file in self.files:
                labelmap = imread(self.folder + self.labelmap_folder + '/' + file)
                intensity_img = img_as_ubyte(imread(self.folder + channel_to_count + file))
                counter = IntensityCounter(labelmap, intensity_img)
                counter.get_cellular_subset(threshold_mean=self.thresholds_mean[i], threshold_max=self.thresholds_max[i], mode=self.mode) 
                counter.get_count()
                self.add_to_results(file, self.channels_to_use[i], counter.valid_labels, counter.count)
                self.save_images(counter.new_labelmap, intensity_img, self.segmentation_folders[i], file)
        self.save_results()

    def add_to_results(self, file, name, valid_labels, count):
        self.results[file]['labels_' + name] = self.make_label_dict(valid_labels)
        self.results[file]['count_nuclei_' + name] = count


    def make_label_dict(self, valid_labels):
        new_dict = {}
        for i in range(len(valid_labels)):
            new_dict[i] = valid_labels[i]
        return new_dict

    
    def make_summary(self):
        self.summary = {}
        for sample, data in self.results.items():
            summary = {}
            for key, value in data.items():
                if not 'labels' in key:
                    summary[key] = value
            self.summary[sample] = summary
        return self.summary


    def save_results(self):
        self.make_summary()
        with open(self.folder + 'results.json', mode='w') as f:
            json.dump(self.results, f)
        
        with open(self.folder + 'result_summary.json', mode='w') as f:
            json.dump(self.summary, f)
        
        df = pd.DataFrame(self.summary).T
        df.to_excel(self.folder + 'results.xlsx')
    

    def get_outlines(self, original_img, label_img):
        outline_image = np.zeros((original_img.shape[0], original_img.shape[1], original_img.shape[2], 3))
        print(outline_image.shape)
        for i in range(outline_image.shape[0]):
            outline_image[i,:,:,:] = mark_boundaries(original_img[i,:,:], label_img[i,:,:])
        return img_as_ubyte(outline_image[:,:,:,0])

    
    def save_images(self, new_labelmap, segmentation_img, save_folder, file_name):
        original_img = segmentation_img
        label_img = new_labelmap
        combined = self.get_outlines(original_img, label_img)
        imsave(save_folder + file_name, combined)

