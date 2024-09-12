import os
from . import download
from .AudioDataset import AudioDataset

# Global parameter
# We will filter out files shorter than that
NUMBER_OF_SECONDS = 1
# In nsynth all the sources are at 16K Hz
RATE = 16000
# DIRS = ['nsynth-test', 'nsynth-valid', 'nsynth-train']
DIRS = ['nsynth-test']
MIN_FILE_SIZE = 10000
'''
This is a public dataset containing instrument sounds from the NSynth dataset.
For more information, please refer to the following paper:
@inproceedings{engel2017neural,
  title={Neural audio synthesis of musical notes with wavenet autoencoders},
  author={Engel, Jesse and Resnick, Cinjon and Roberts, Adam and Dieleman, Sander and Norouzi, Mohammad and Eck, Douglas and Simonyan, Karen},
  booktitle={International Conference on Machine Learning},
  pages={1068--1077},
  year={2017},
  organization={PMLR}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='nsynth', *args, **kwargs):
        self.path = path
                
        self.all_dirs = {d:os.path.join(self.path,d) for d in DIRS if os.path.isdir(os.path.join(self.path,d))}
        assert len(self.all_dirs)>0 , "No directory found in {}".format(self.path)   
        self.splits = DIRS
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        
        

# Links to the audio files
REMOTES = {
    "train": download.RemoteFileMetadata(
        filename="nsynth-train.jsonwav.tar.gz",
        url="http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-train.jsonwav.tar.gz",
        checksum="fde6665a93865503ba598b9fac388660",
    ),
    "valid": download.RemoteFileMetadata(
        filename="nsynth-valid.jsonwav.tar.gz",
        url="http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-valid.jsonwav.tar.gz",
        checksum="87e94a00a19b6dbc99cf6d4c0c0cae87",
    ),
    "test": download.RemoteFileMetadata(
        filename="nsynth-test.jsonwav.tar.gz",
        url="http://download.magenta.tensorflow.org/datasets/nsynth/nsynth-test.jsonwav.tar.gz",
        checksum="5e6f8719bf7e16ad0a00d518b78af77d",
    ),
}



