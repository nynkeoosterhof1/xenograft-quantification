
from skimage.measure import regionprops
import numpy as np
from skimage.util import img_as_uint


class IntensityCounter():

    def __init__(self, labelmap, intensity_image):
        self.labels = labelmap
        self.intensity_image = intensity_image
        self.new_labelmap = np.zeros(self.labels.shape)
        self.regionprops = regionprops(self.labels, intensity_image=self.intensity_image)
        self.valid_labels = []
        self.count = 0

    def get_cellular_subset(self, threshold_mean=5, threshold_max=20, mode='mean'):
        for prop in self.regionprops:
            if mode == 'max':
                if prop['intensity_max'] > threshold_max:
                    self.valid_labels.append(prop['label'])
            elif mode == 'mean':
                if prop['intensity_mean'] > threshold_mean:
                    self.valid_labels.append(prop['label'])
            elif mode == 'mean/max':
                if prop['intensity_max'] > threshold_max and prop['intensity_mean'] > threshold_mean:
                    self.valid_labels.append(prop['label'])

    
    def get_selected_label_image(self):
        for label in self.valid_labels:
            self.new_labelmap[self.labels == label] = label
        self.new_labelmap = self.new_labelmap.astype(dtype=np.uint16)
        


    def get_count(self):
        self.count = len(self.valid_labels)
        self.get_selected_label_image()
        