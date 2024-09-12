import os
from . import download
from .AudioDataset import AudioDataset
from . import thyolo_noise
'''
This is a public dataset containing thyolo calls.
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
class Dataset(thyolo_noise.Dataset):
    def __init__(self, conf, path, dname='thyolo', *args, **kwargs):
        self.all_dirs = {'all':os.path.join(path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "annotations": download.RemoteFileMetadata(
        filename="Annotations.zip",
        url="https://zenodo.org/record/6328244/files/Annotations.zip?download=1",
        checksum="68a74edb724c90fd6010ff8e3ea8a4f9",
    ),
    "audio": download.RemoteFileMetadata(
        filename="Audio.zip",
        url="https://zenodo.org/record/6328244/files/Audio.zip?download=1",
        checksum="5ccf10e4de716a5f583eea591d49f220",
    ),
}


