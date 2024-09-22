import os

from file_manager import FileManager
from lif_unpacker import LifUnpacker

class ImageUnpacker(FileManager):
    
    def __init__(self, folder_path):
        super().__init__(folder_path)
        
    def unpack_images(self):
        if self.has_lif:
            self.unpack_lifs()

    def unpack_lifs(self):
        lifs = [file for file in os.listdir(self.folder) if file.endswith('.lif')]
        for lif in lifs:
            file = LifUnpacker(self.folder, lif)
            file.unpack_images()

    