import os
from . import download
from .AudioDataset import AudioDataset
from . import xeno_canto_labeled_noise
''' 
This is a public subset of xeno-canto dataset containing detection labels for bird songs.
For more information, please access the following paper:
@dataset{jeantet_lorene_2023_7828148,
  author       = {Jeantet Lorene and
                  Dufourq Emmanuel},
  title        = {{Manually labeled Bird song dataset of 22 species 
                   from Xeno-canto to enhance deep learning acoustic
                   classifiers with contextual information.}},
  month        = apr,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7828148},
  url          = {https://doi.org/10.5281/zenodo.7828148}
}
'''
class Dataset(xeno_canto_labeled_noise.Dataset):
    def __init__(self, conf, path, dname='xeno_canto_labeled', *args, **kwargs):
        self.all_dirs = {'all':os.path.join(path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "annotation": download.RemoteFileMetadata(
        filename="Annotation.zip",
        url="https://zenodo.org/record/7828148/files/Annotation.zip?download=1",
        checksum="31606f08b7001d93a4a7796dd77ae18e",
    ),
    "audio": download.RemoteFileMetadata(
        filename="Audio.zip",
        url="https://zenodo.org/record/7828148/files/Audio.zip?download=1",
        checksum="17260b6dbffb367dfaf57d609089cf75",
    ),
}



