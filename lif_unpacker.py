import read_lif
from skimage.io import imsave
from skimage.util import img_as_uint
from file_manager import FileManager


class LifUnpacker(FileManager):

    def __init__(self, folder_path, file_name, only_z_stack=True):

        super().__init__(folder_path)

        self.folder_path = folder_path
        self.lif_path = folder_path + file_name
        self.file_name = file_name.split('.')[0]
        self.reader = read_lif.Reader(self.lif_path)
        self.images = self.get_images_lif_file(self.reader) 
        self.output_folder = self.make_new_folder(self.folder_path, self.file_name) 
        self.z_stack = only_z_stack

    def get_images_lif_file(self, reader):
        return reader.getSeries() 
    
    def save_image_as_tiff(self, image_path, image):
        imsave(image_path, img_as_uint(image))

    def unpack_image(self, image):
        image_name = image.getName()
        channels = image.getChannels()
        
        if image.hasZ():
            for channel in range(len(channels)):
                channel_name = channels[channel].getAttribute('LUTName')
                new_path = self.make_new_folder(self.output_folder, channel_name)
                z_stack = image.getFrame(channel=channel)
                image_path = new_path + image_name + '.tif'
                self.save_image_as_tiff(image_path, z_stack)

 
    def unpack_images(self):
        for image in self.images:
            self.unpack_image(image)