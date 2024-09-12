'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a public domain dataset containing macaque vocalizations.
For more information, please refer to the following paper:
@article{fukushima2015distributed,
  title={Distributed acoustic cues for caller identity in macaque vocalization},
  author={Fukushima, Makoto and Doyle, Alex M and Mullarkey, Matthew P and Mishkin, Mortimer and Averbeck, Bruno B},
  journal={Royal Society open science},
  volume={2},
  number={12},
  pages={150432},
  year={2015},
  publisher={The Royal Society Publishing}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='macaques', *args, **kwargs):
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
    "zip": download.RemoteFileMetadata(
        filename="macaques.zip",
        url="https://archive.org/download/macaque_coo_calls/macaques.zip",
        checksum="f353f93a955ea8fc81e3bd82b2c6fc81",
    )
}



