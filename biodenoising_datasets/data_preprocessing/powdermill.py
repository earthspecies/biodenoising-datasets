import os
from . import download
from .AudioDataset import AudioDataset
from . import powdermill_noise
'''
This is a public dataset for bird call detection.
For more information, please access the following paper:
@dataset{chronister_2021_4656848,
  author       = {Chronister, Lauren M. and
                  Rhinehart, Tessa A. and
                  Place, Aidan and
                  Kitzes, Justin},
  title        = {{An annotated set of audio recordings of Eastern 
                   North American birds containing frequency, time,
                   and species information}},
  month        = apr,
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5061/dryad.d2547d81z},
  url          = {https://doi.org/10.5061/dryad.d2547d81z}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='powdermill', *args, **kwargs):
        self.path = path
        process = powdermill_noise.Dataset.__dict__["process"]
        self.process_file = powdermill_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="wav_Files.zip",
        url="https://zenodo.org/record/4656848/files/wav_Files.zip?download=1s",
        checksum="2876c0cfc6ace1845ac04814ea9180f1",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotation_Files.zip",
        url="https://zenodo.org/record/4656848/files/annotation_Files.zip?download=1",
        checksum="8f78ba7cf9fc5d25656f7747ed3406d1",
    ),
}



