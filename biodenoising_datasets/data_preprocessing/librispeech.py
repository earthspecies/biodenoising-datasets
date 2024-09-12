import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset containing human speech from LibriSpeech.
For more information, please refer to the following paper:
@inproceedings{panayotov2015librispeech,
  title={Librispeech: an asr corpus based on public domain audio books},
  author={Panayotov, Vassil and Chen, Guoguo and Povey, Daniel and Khudanpur, Sanjeev},
  booktitle={2015 IEEE international conference on acoustics, speech and signal processing (ICASSP)},
  pages={5206--5210},
  year={2015},
  organization={IEEE}
}
'''
# Global parameter
# We will filter out files shorter than that
NUMBER_OF_SECONDS = 3
# In LibriSpeech all the sources are at 16K Hz
RATE = 16000
DIRS = ['dev-clean', 'test-clean','train-clean-360']
MIN_FILE_SIZE = 10000

class Dataset(AudioDataset):
    def __init__(self, conf, dname='librispeech', *args, **kwargs):
        self.all_dirs = {d:os.path.join(conf["input"][dname]["path"],d) for d in DIRS if os.path.isdir(os.path.join(conf["input"][dname]["path"],d))}
        assert len(self.all_dirs)>0 , "No directory found in {}".format(conf["input"][dname]["path"])   
        self.splits = DIRS
        super(Dataset, self).__init__(conf, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "train-clean-360": download.RemoteFileMetadata(
        filename="train-clean-360.tar.gz",
        url="https://www.openslr.org/resources/12/train-clean-360.tar.gz",
        checksum="c0e676e450a7ff2f54aeade5171606fa",
    ),
    "dev-clean": download.RemoteFileMetadata(
        filename="dev-clean.tar.gz",
        url="https://www.openslr.org/resources/12/dev-clean.tar.gz",
        checksum="42e2234ba48799c1f50f24a7926300a1",
    ),
    "test-clean": download.RemoteFileMetadata(
        filename="test-clean.tar.gz",
        url="https://www.openslr.org/resources/12/test-clean.tar.gz",
        checksum="32fa31d27d2e1cad72775fee3f4849a9",
    ),
}
