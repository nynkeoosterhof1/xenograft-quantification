from msilib.schema import File
from sample_cell_counter import SampleCellCounter
from file_manager import FileManager
import json
import pandas as pd
import os

class DataCellCounter(FileManager):

    def __init__(self, path_folder, labelmaps_2D, labelmaps_3D, threshold_ratio=0.8, threshold_size=300):
        super().__init__(path_folder)
        self.subfolders = self.get_subfolders(self.folder)
        self.folder_labelmaps_2D = labelmaps_2D 
        self.folder_labelmaps_3D = labelmaps_3D
        self.threshold_ratio = threshold_ratio
        self.threshold_size = threshold_size
        self.results = {}

    def analyze_data(self):
        for folder in self.subfolders:
            counter = SampleCellCounter(folder, self.folder_labelmaps_2D, self.folder_labelmaps_3D)
            counter.analyze_sample()
            counter.save_results()
        self.save_results()    


    def make_result_summary(self):
        for folder in self.subfolders:
            with open(folder + 'result_summary.json', mode='r') as f:
                result = json.load(f)
                for sample, data in result.items():
                    self.results[sample] = data

    
    def save_results(self):
        self.make_result_summary()
        with open(self.folder + 'result_summary.json', mode='w') as f:
            json.dump(self.results, f)
        
        df = pd.DataFrame(self.results).T
        df.to_excel(self.folder + 'results.xlsx')




