import os
from . import download
from .AudioDataset import AudioDataset
from . import whydah_noise
'''
This is a public dataset containing whydah calls.
For more information, please access the following paper:
@article{dufourq2022passive,
  title={Passive acoustic monitoring of animal populations with transfer learning},
  author={Dufourq, Emmanuel and Batist, Carly and Foquet, Ruben and Durbach, Ian},
  journal={Ecological Informatics},
  volume={70},
  pages={101688},
  year={2022},
  publisher={Elsevier}
}
'''
class Dataset(whydah_noise.Dataset):
    def __init__(self, conf, path, dname='whydah', *args, **kwargs):
        self.all_dirs = {'all':os.path.join(path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "annotations": download.RemoteFileMetadata(
        filename="Annotations.zip",
        url="https://zenodo.org/record/6330711/files/Annotations.zip?download=1",
        checksum="7971c980656775a615d64d8d754dab99",
    ),
    "audio": download.RemoteFileMetadata(
        filename="Audio.zip",
        url="https://zenodo.org/record/6330711/files/Audio.zip?download=1",
        checksum="2d93245786f9f17e5717c4b890d3196d",
    ),
}



