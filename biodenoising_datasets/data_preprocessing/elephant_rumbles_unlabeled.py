import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a private ESP dataset containing unlabeled elephant rumbles.
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='elephant_rumbles_unlabeled', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="elephant_rumbles_unlabeled.zip",
        url="gs://ml-bioacoustics-datasets/elephant_rumbles_unlabeled.zip",
        checksum="fc43c462829f04d906a802887f54f298",
    )
}



