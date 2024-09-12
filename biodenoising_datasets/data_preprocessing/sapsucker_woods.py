import os
from . import download
from .AudioDataset import AudioDataset
from . import sapsucker_woods_noise
'''
This is a public dataset for bird call detection.
For more information, please access the following paper:
@dataset{stefan_kahl_2022_7079380,
  author       = {Stefan Kahl and
                  Russell Charif and
                  Holger Klinck},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from the Northeastern United States}},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = 2,
  doi          = {10.5281/zenodo.7079380},
  url          = {https://doi.org/10.5281/zenodo.7079380}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='sapsucker_woods', *args, **kwargs):
        self.path = path
        process = sapsucker_woods_noise.Dataset.__dict__["process"]
        self.process_file = sapsucker_woods_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7079380/files/soundscape_data.zip?download=1",
        checksum="4dc5a3e83494a638d80bc7b3d1517137",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7079380/files/annotations.csv?download=1",
        checksum="517eb9700f88ec9ac054a8aec7c805ec",
    ),
}



