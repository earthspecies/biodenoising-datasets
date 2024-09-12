'''
DO NOT USE - some calls are not annotated and they end up in the noise class
'''
import os
import torch
import pandas as pd
import torchaudio
import scipy
import numpy as np
from . import download
from . import orcasound_skrw_labeled_noise
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orcasound project. This subset contains orca vocalizations.
For more information, please access the website: 
https://www.orcasound.net/
'''
NOISE_BLACKLIST = []
MIN_DURATION = 2. #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.2 #seconds - add a tail to the audio files to avoid cutting the end of the whale sound
FRONT = 0.05 #seconds - add a front to the audio files to avoid cutting the beginning of the whale sound

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orca_skrw_labeled', *args, **kwargs):
        self.path = path
        process = orcasound_skrw_labeled_noise.Dataset.__dict__["process"]
        self.process_file = orcasound_skrw_labeled_noise.Dataset.__dict__["process_file"]
        process(self,conf, dname)
        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "all": 
        download.RemoteFileMetadata(
            filename="TrainDataLatest_PodCastAllRounds_123567910.tar.gz",
            url="s3://acoustic-sandbox/labeled-data/detection/train/TrainDataLatest_PodCastAllRounds_123567910.tar.gz",
            checksum="93b7c1adf73b1c054b6acd9a5f307f79",
        )
}
