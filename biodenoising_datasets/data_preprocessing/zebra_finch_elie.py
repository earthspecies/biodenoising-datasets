import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a dataset containing the zebra finch recordings from the paper:
@article{elie2016vocal,
  title={The vocal repertoire of the domesticated zebra finch: a data-driven approach to decipher the information-bearing acoustic features of communication signals},
  author={Elie, Julie E and Theunissen, Frederic E},
  journal={Animal cognition},
  volume={19},
  pages={285--315},
  year={2016},
  publisher={Springer}
}
The dataset is not directly downloable and it is described at: https://github.com/earthspecies/library/tree/main/zebra_finch
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='zebra_finch', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="zebra_finch.zip",
        url="gs://ml-bioacoustics-datasets/zebra_finch.zip",
        checksum="fb9a3ed2eb9360002df188ef71bdf32c",
    )
}



