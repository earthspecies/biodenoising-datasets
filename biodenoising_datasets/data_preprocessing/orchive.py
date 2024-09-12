import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orchive project. This subset contains orca vocalizations.
For more information, please access the following paper:
@article{ness2013orchive,
  title={The Orchive: Data mining a massive bioacoustic archive},
  author={Ness, Steven and Symonds, Helena and Spong, Paul and Tzanetakis, George},
  journal={arXiv preprint arXiv:1307.0589},
  year={2013}
}
The dataset is described at: https://github.com/earthspecies/library/tree/main/orcas
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orchive', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        self.all_dirs = {'all':os.path.join(self.path,'orchive-dataset','call-catalog-xsilence','aiff')}
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "orchive": download.RemoteFileMetadata(
        filename="orchive-dataset.tar.gz",
        url="https://storage.googleapis.com/ml-bioacoustics-datasets/orchive-dataset.tar.gz",
        checksum="daa5965ba3d878b96f6f14b2e84215fd",
    )
}
