'''
Dataset derived from Xenocanto by separating the audio files with bird-mixit and remixing together the files with similar predictions using yamnet.
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a wrapper for the xeno-canto dataset.
The dataset is not directly accessible from the internet. 
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='xenocanto', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="dir",
        url="gs://xeno-canto/A/",
        checksum="",
    )
}



