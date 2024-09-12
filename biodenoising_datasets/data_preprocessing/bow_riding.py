'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
Private ESP dataset for bow riding.
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='bow_riding', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="Bow\ Riding\ Data\ Set.zip",
        url="gs://bow_riding/Bow\ Riding\ Data\ Set.zip",
        checksum="fdsfsdfsdfdsfsdfdsfsdfdsf",
    )
}



