import os
from . import download
from .AudioDataset import AudioDataset
from . import sierra_nevada_noise
'''
This is a public dataset for bird call detection.
For more information, please access the following paper:
@dataset{stefan_kahl_2022_7050014,
  author       = {Stefan Kahl and
                  Connor M. Wood and
                  Philip Chaon and
                  M. Zachariah Peery and
                  Holger Klinck},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from the Western United States}},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.7050014},
  url          = {https://doi.org/10.5281/zenodo.7050014}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='sierra_nevada', *args, **kwargs):
        self.path = path
        process = sierra_nevada_noise.Dataset.__dict__["process"]
        self.process_file = sierra_nevada_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7050014/files/soundscape_data.zip?download=1",
        checksum="2874bdb56f18002a0e5b6fe2402b3c0b",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7050014/files/annotations.csv?download=1",
        checksum="36adcb398a1b82d9b165d62f09d31b31",
    ),
}



