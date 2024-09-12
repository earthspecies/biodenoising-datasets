'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
from . import lemur_noise
'''
This is a public dataset containg lemur vocalizations.
For more information, please refer to the following paper:
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
class Dataset(lemur_noise.Dataset):
    def __init__(self, conf, path, dname='lemur', *args, **kwargs):
        self.all_dirs = {'all':os.path.join(path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "annotations1": download.RemoteFileMetadata(
        filename="Annotations1.zip",
        url="https://zenodo.org/record/6331594/files/Annotations1.zip?download=1",
        checksum="1a4f202beec54e2892d0f762d96ce613",
    ),
    "annotations2": download.RemoteFileMetadata(
        filename="Annotations2.zip",
        url="https://zenodo.org/record/6331594/files/Annotations2.zip?download=1",
        checksum="7637e2b3934c5cf56ef1431f15ae6440",
    ),
    "annotations3": download.RemoteFileMetadata(
        filename="Annotations3.zip",
        url="https://zenodo.org/record/6331594/files/Annotations3.zip?download=1",
        checksum="3de9d2350b7bc791d6783dcd268cd608",
    ),
    "audio1": download.RemoteFileMetadata(
        filename="Audio1.zip",
        url="https://zenodo.org/record/6331594/files/Audio1.zip?download=1",
        checksum="d5759942065acc1cb02d662ad33c4885",
    ),
    "audio2": download.RemoteFileMetadata(
        filename="Audio2.zip",
        url="https://zenodo.org/record/6331594/files/Audio2.zip?download=1",
        checksum="6d52bd36f9e0c0b35cf8c10bef67ca33",
    ),
    "audio3": download.RemoteFileMetadata(
        filename="Audio3.zip",
        url="https://zenodo.org/record/6331594/files/Audio3.zip?download=1",
        checksum="8c3b10dec6c54a36f5016440ceb3efd8",
    )
}


