import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset containing speech sounds from the VCTK dataset.
For more information, please access the following paper:
@article{veaux2017cstr,
  title={CSTR VCTK corpus: English multi-speaker corpus for CSTR voice cloning toolkit},
  author={Veaux, Christophe and Yamagishi, Junichi and MacDonald, Kirsten and others},
  journal={University of Edinburgh. The Centre for Speech Technology Research (CSTR)},
  volume={6},
  pages={15},
  year={2017}
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
    def __init__(self, conf, dname='vctk96', *args, **kwargs):
        super(Dataset, self).__init__(conf, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "wav1": download.RemoteFileMetadata(
        filename="wav-1.zip",
        url="https://datashare.ed.ac.uk/bitstream/handle/10283/2774/wav-1.zip?sequence=1&isAllowed=y",
        checksum="d2a3c39095825c6b962034904bf08642",
    ),
    "wav2": download.RemoteFileMetadata(
        filename="wav-2_and_wav-3.zip",
        url="https://datashare.ed.ac.uk/bitstream/handle/10283/2774/wav-2_and_wav-3.zip?sequence=2&isAllowed=y",
        checksum="68341f3dc4e1dbf33a9d3f2b261c92fe",
    ),
}
