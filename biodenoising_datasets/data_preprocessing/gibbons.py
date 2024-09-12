import os
from . import download
from .AudioDataset import AudioDataset
from . import gibbons_noise
'''
This is a public dataset of gibbons vocalizations.
For more info check the paper:
@article{jeantet2023improving,
  title={Improving deep learning acoustic classifiers with contextual information for wildlife monitoring},
  author={Jeantet, Lorene and Dufourq, Emmanuel},
  journal={Ecological Informatics},
  volume={77},
  pages={102256},
  year={2023},
  publisher={Elsevier}
} 
'''
class Dataset(gibbons_noise.Dataset):
    def __init__(self, conf, path, dname='gibbons', *args, **kwargs):
        self.all_dirs = {'all':os.path.join(path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "annotations": download.RemoteFileMetadata(
        filename="Annotations.zip",
        url="https://zenodo.org/record/7997739/files/Annotations.zip?download=1",
        checksum="edc5fd17c860d9bbafc8895a90da28fd",
    ),
    "audio1": download.RemoteFileMetadata(
        filename="Audio_1.zip",
        url="https://zenodo.org/record/7997739/files/Audio_1.zip?download=1",
        checksum="348936dbac82e46651eb703ac0f1223d",
    ),
    "audio2": download.RemoteFileMetadata(
        filename="Audio_2.zip",
        url="https://zenodo.org/record/7997739/files/Audio_2.zip?download=1",
        checksum="54bf496b776a612d206d8bd5a6f692ac",
    ),
    "audio3": download.RemoteFileMetadata(
        filename="Audio_3.zip",
        url="https://zenodo.org/record/7997739/files/Audio_3.zip?download=1",
        checksum="264c67854af78a2aa99a58d830960500",
    ),
    "audio4": download.RemoteFileMetadata(
        filename="Audio_4.zip",
        url="https://zenodo.org/record/7997739/files/Audio_4.zip?download=1",
        checksum="4a3ff80d3f13b3c47e218a5c0a15a419",
    )
}



