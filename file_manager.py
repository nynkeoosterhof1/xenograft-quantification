import os
import glob
import json
from statistics import mode


class FileManager():

    def __init__(self, path_folder):
        self.folder = path_folder
        self.has_lif = self.has_lifs()
        
    def get_lif_files(self):
        for name in glob.glob(self.folder + '*.lif'):
            file_path = self.folder + os.path.basename(name)
            self.lif_files.append(file_path) 
 
    def make_new_folder(self, path, folder_name):
        if not os.path.exists(path + folder_name):
            os.makedirs(path + folder_name, exist_ok=True)
        return path + folder_name + '/'
    
    def has_lifs(self):
        for file in os.listdir(self.folder):
            if file.endswith('.lif'):
                return True
        return False 
    
    def get_subfolders(self, path):
        return [path + subfolder + '/' for subfolder in os.listdir(path) if os.path.isdir(os.path.join(path, subfolder))]
    
    
    def get_folder_name(self, folder_path):
        return folder_path.split('/')[-2]
    
    def remove_files(self, path):
        files = glob.glob(path + '*')
        for f in files:
            os.remove(f)
    
    def open_json(self, file_name):
        with open(self.folder + file_name, mode='r') as f:
            results = json.load(f)
        return results
    

