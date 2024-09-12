'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public domain dataset containing infant marmoset vocalizations.
@article{gultekin2021high,
  title={High plasticity in marmoset monkey vocal development from infancy to adulthood},
  author={Gultekin, Yasemin B and Hildebrand, David GC and Hammerschmidt, Kurt and Hage, Steffen R},
  journal={Science Advances},
  volume={7},
  number={27},
  pages={eabf2938},
  year={2021},
  publisher={American Association for the Advancement of Science}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='infant_marmoset', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "zip1": download.RemoteFileMetadata(
        filename="InfantMarmosetsVox_twin_1.tar.gz",
        url="https://zenodo.org/records/10130104/files/InfantMarmosetsVox_twin_1.tar.gz?download=1",
        checksum="f98ecec5ce6a83c12eb801e660b27a7c",
    ),
}



