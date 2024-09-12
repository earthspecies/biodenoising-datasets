import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset containing singing voices from the VocalSet dataset.
For more information, please access the following paper:
@inproceedings{wilkins2018vocalset,
  title={VocalSet: A Singing Voice Dataset.},
  author={Wilkins, Julia and Seetharaman, Prem and Wahl, Alison and Pardo, Bryan},
  booktitle={ISMIR},
  pages={468--474},
  year={2018}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='vocalset', *args, **kwargs):
        self.path = os.path.join(path,'FULL')
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "Vocalset1": download.RemoteFileMetadata(
        filename="VocalSet11.zip",
        url="https://zenodo.org/record/1442513/files/VocalSet11.zip?download=1",
        checksum="0c09396242f946e7111ad7d8fc649b81",
    ),
    # "Vocalset2": download.RemoteFileMetadata(
    #     filename="VocalSet1-2.zip",
    #     url="https://zenodo.org/record/1442513/files/VocalSet1-2.zip?download=1",
    #     checksum="c5e5efab412637fc94972b93c343a2f0",
    # ),
    # "annotations": download.RemoteFileMetadata(
    #     filename="Annotated%20VocalSet.zip",
    #     url="https://zenodo.org/record/7061507/files/Annotated%20VocalSet.zip?download=1",
    #     checksum="f4324592f5edebcb9e572c01531ac63b",
    # )
}


