'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a ESP private dataset of minke detections from the HiCEAS project.
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='hiceas_minke', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="hiceas_1-20_minke-detection.zip",
        url="gs://ml-bioacoustics-datasets/hiceas_1-20_minke-detection.zip",
        checksum="0b596ecabd9dda254c2c2c72545592f0",
    )
}



