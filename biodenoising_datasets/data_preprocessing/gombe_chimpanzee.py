'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset of gombe chimpanzee vocalizations.
For more info check the paper: 
@article{desai2021chimpanzee,
  title={Chimpanzee pant-hoots encode information about individual but not group differences},
  author={Desai, Nisarg P and Fedurek, Pawel and Slocombe, Katie E and Wilson, Michael L},
  journal={bioRxiv},
  pages={2021--03},
  year={2021},
  publisher={Cold Spring Harbor Laboratory}
}
The dataset is obtained from https://archive.org/details/chimpanzee-vocalizations 
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='gombe_chimpanzee', *args, **kwargs):
        self.path = path
        # #generate dataset if not already done
        # self.process(conf, dname, *args, **kwargs)

        # self.all_dirs = {'all':os.path.join(self.path,'audio')}
        # self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    # def process(self, conf, dname):
    #     audio_noise = os.path.join(self.path,'audio')
    #     os.makedirs(audio_noise, exist_ok=True)
    #     df = pd.read_pickle(os.path.join(self.path,'annotations.pkl.gzip'))
        
            

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="Chimpanzee%20vocalizations.zip",
        url="https://archive.org/download/chimpanzee-vocalizations/Chimpanzee%20vocalizations.zip",
        checksum="eeac32dba58b9f5f5370a838a5cc0719",
    ),
}



