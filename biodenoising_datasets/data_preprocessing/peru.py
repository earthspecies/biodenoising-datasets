'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
from . import peru_noise
'''
This is a public dataset for bird call detection.
For more information, please access the following paper:
@dataset{w_alexander_hopping_2022_7079124,
  author       = {W. Alexander Hopping and
                  Stefan Kahl and
                  Holger Klinck},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from the Southwestern Amazon Basin}},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.7079124},
  url          = {https://doi.org/10.5281/zenodo.7079124}
}
'''
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound


class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='peru', *args, **kwargs):
        self.path = path
        process = peru_noise.Dataset.__dict__["process"]
        self.process_file = peru_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
            

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7079124/files/soundscape_data.zip?download=1",
        checksum="bd01e1caba1b720c5856a3bd57d220d3",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7079124/files/annotations.csv?download=1",
        checksum="2ab1a54b35ba0b6df8a4c91a48a1b684",
    ),
}



