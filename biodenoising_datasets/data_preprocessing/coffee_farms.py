'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
from . import coffee_farms_noise
'''
This is a public dataset for benchmarking bird sound detection.
For more information check the paper:
@dataset{alvaro_vega_hidalgo_2023_7525349,
  author       = {Álvaro Vega-Hidalgo and
                  Stefan Kahl and
                  Laurel B. Symes and
                  Viviana Ruiz-Gutiérrez and
                  Ingrid Molina-Mora and
                  Fernando Cediel and
                  Luis Sandoval and
                  Holger Klinck},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from neotropical coffee farms in
                   Colombia and Costa Rica}},
  month        = jan,
  year         = 2023,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.7525349},
  url          = {https://doi.org/10.5281/zenodo.7525349}
}
The dataset is available at the following link:
https://zenodo.org/records/7525349
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='coffee_farms', *args, **kwargs):
        self.path = path
        process = coffee_farms_noise.Dataset.__dict__["process"]
        self.process_file = coffee_farms_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7525349/files/soundscape_data.zip?download=1",
        checksum="15a00bb3221e56ec83d38ad04c26ce68",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7525349/files/annotations.csv?download=1",
        checksum="f72be6c60b530fb622ea954627edea47",
    ),
}



