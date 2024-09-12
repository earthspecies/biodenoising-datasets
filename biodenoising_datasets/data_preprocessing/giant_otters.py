import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset of giant otters vocalizations.
For more info check the paper:
@article{mumm2014vocal,
  title={The vocal repertoire of adult and neonate giant otters (Pteronura brasiliensis)},
  author={Mumm, Christina AS and Kn{\"o}rnschild, Mirjam},
  journal={PloS one},
  volume={9},
  number={11},
  pages={e112562},
  year={2014},
  publisher={Public Library of Science San Francisco, USA}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='giant_otters', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="giant_otters.zip",
        url="https://archive.org/download/giant_otters/giant_otters.zip",
        checksum="610685f7c192147f0b04c662d1080de9",
    )
}



