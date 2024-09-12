'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a private ESP dataset containing geladas vocalizations.
For more info check the paper:
@article{gustison2012derived,
  title={Derived vocalizations of geladas (Theropithecus gelada) and the evolution of vocal complexity in primates},
  author={Gustison, Morgan L and le Roux, Aliza and Bergman, Thore J},
  journal={Philosophical Transactions of the Royal Society B: Biological Sciences},
  volume={367},
  number={1597},
  pages={1847--1859},
  year={2012},
  publisher={The Royal Society}
}

'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='geladas', *args, **kwargs):
        self.path = path
        # #generate dataset if not already done
        # self.process(conf, dname, *args, **kwargs)

        # self.all_dirs = {'all':os.path.join(self.path,'audio')}
        # self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    # def process(self, conf, dname):
    #     audio_noise = os.path.join(self.path,'audio')
    #     os.makedirs(audio_noise, exist_ok=True)
    #     df = pd.read_pickle(os.path.join(self.path,s'annotations.pkl.gzip'))
        
            

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="GustisonBergman_GeladaData.zip",
        url="gs://geladas/GustisonBergman_GeladaData.zip",
        checksum="733ce0e85815a20a61a17bfa0c55c208",
    )
}



