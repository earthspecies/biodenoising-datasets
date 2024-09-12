import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a public dataset for avian flight call detection.
For more information check the paper:
@inproceedings{lostanlen2018icassp,
  title = {BirdVox-full-night: a dataset and benchmark for avian flight call detection},
  author = {Lostanlen, Vincent and Salamon, Justin and Farnsworth, Andrew and Kelling, Steve and Bello, Juan Pablo},
  booktitle = {Proc. IEEE ICASSP},
  year = {2018},
  published = {IEEE},
  venue = {Calgary, Canada},
  month = {April},
}
The dataset is downloaded from the following link:
https://zenodo.org/records/1205569
'''

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='birdvox_night', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="BirdVox-full-night_flac-audio_unit01.flac",
        url="https://zenodo.org/record/1205569/files/BirdVox-full-night_flac-audio_unit01.flac?download=1",
        checksum="453ea014550936dec2af285f21df131c",
    )
}



