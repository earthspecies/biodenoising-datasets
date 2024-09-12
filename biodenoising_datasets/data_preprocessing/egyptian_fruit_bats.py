'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a public dataset of Egyptian fruit bats vocalizations.
@article{prat2017annotated,
  title={An annotated dataset of Egyptian fruit bat vocalizations across varying contexts and during vocal ontogeny},
  author={Prat, Yosef and Taub, Mor and Pratt, Ester and Yovel, Yossi},
  journal={Scientific data},
  volume={4},
  number={1},
  pages={1--7},
  year={2017},
  publisher={Nature Publishing Group}
}
For more info check the repository https://github.com/earthspecies/library/tree/main/egyptian_fruit_bat
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='egyptian_fruit_bats', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="egyptian_fruit_bats.zip",
        url="https://archive.org/download/egyptian_fruit_bats_10k/egyptian_fruit_bats.zip",
        checksum="3cc423c655500b756ffaa221c4c26d9e",
    ),
}



