import torch
import torchaudio
import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
This is a public dataset for music source separation.
For more information check the paper:
@article{liutkus2014kernel,
  title={Kernel additive models for source separation},
  author={Liutkus, Antoine and Fitzgerald, Derry and Rafii, Zafar and Pardo, Bryan and Daudet, Laurent},
  journal={IEEE Transactions on Signal Processing},
  volume={62},
  number={16},
  pages={4298--4310},
  year={2014},
  publisher={IEEE}
}
'''

class Dataset(AudioDataset):
    def __init__(self, conf, dname='ccmixter_voice', *args, **kwargs):
        self.audio_files = {}
        self.audio_files['all'] = [os.path.join(root,file) for root,fdir,files in os.walk(conf["input"][dname]["path"]) for file in files if file.endswith('source-02.wav') and not file.startswith('.')]
        self.all_dirs = {'all':conf["input"][dname]["path"]}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "zip": 
        download.RemoteFileMetadata(
            filename="ccmixter_corpus.zip",
            url="http://liutkus.net/ccmixter_corpus.zip",
            checksum="231eea133f59f6a7a5ef4c47a8205256",
        ),
}
