from sample_intensity_counter import SampleIntensityCounter
from file_manager import FileManager
import json
import pandas as pd


class DataIntensityCounter(FileManager):

    def __init__(self, path_folder, results_file, labelmap_folder, channels_to_use, mode = 'mean', channel_thresholds_mean = [], channel_thresholds_max=[], preprocessed=True):
        super().__init__(path_folder)
        self.results_file_name_subfolders = results_file
        self.labelmap_folder = labelmap_folder
        self.channels_to_use = channels_to_use
        self.mode = mode
        self.channel_thresholds_mean = channel_thresholds_mean
        self.channel_thresholds_max = channel_thresholds_max
        self.preprocessed = preprocessed
        self.subfolders = self.get_subfolders(self.folder)
        self.results = {}

    
    def count_cells(self):
        for folder in self.subfolders:
            counter = SampleIntensityCounter(folder, 'results.json', self.labelmap_folder, self.channels_to_use, self.mode, self.channel_thresholds_mean, self.channel_thresholds_max, self.preprocessed)
            counter.count_cells()
        self.save_results()
        
    
    def make_result_summary(self):
        for folder in self.subfolders:
            folder_name = self.get_folder_name(folder)
            with open(folder + 'result_summary.json', mode='r') as f:
                result = json.load(f)
                for sample, data in result.items():
                    self.results[folder_name + '_' + sample] = data

    
    def save_results(self):
        self.make_result_summary()
        with open(self.folder + 'result_summary.json', mode='w') as f:
            json.dump(self.results, f)
        
        df = pd.DataFrame(self.results).T
        df.to_excel(self.folder + 'results.xlsx')
