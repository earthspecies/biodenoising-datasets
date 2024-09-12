'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
from . import high_sierras_noise
'''
This is a public dataset of high Sierras birds recordings.
For more info check the paper:
@dataset{mary_clapp_2023_7525805,
  author       = {Mary Clapp and
                  Stefan Kahl and
                  Erik Meyer and
                  Megan McKenna and
                  Holger Klinck and
                  Gail Patricelli},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from the southern Sierra Nevada
                   mountain range}},
  month        = jan,
  year         = 2023,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.7525805},
  url          = {https://doi.org/10.5281/zenodo.7525805}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='high_sierras', *args, **kwargs):
        self.path = path
        process = high_sierras_noise.Dataset.__dict__["process"]
        self.process_file = high_sierras_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7525805/files/soundscape_data.zip?download=1",
        checksum="b7796e5e28d1f6b1a8bb16f0ba294c9d",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7525805/files/annotations.csv?download=1",
        checksum="0f300f5536784cc34f51f9f42e80756e",
    ),
}



