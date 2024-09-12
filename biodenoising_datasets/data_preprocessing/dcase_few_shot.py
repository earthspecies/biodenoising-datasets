import os
from . import download
from .AudioDataset import AudioDataset
from . import dcase_few_shot_noise
import torchaudio
import numpy as np
import pandas as pd
'''
This is a public dataset for benchmarking few-shot bioacoustic event detection.
For more information check the paper:
@article{nolasco2022few,
  title={Few-shot bioacoustic event detection at the DCASE 2022 challenge},
  author={Nolasco, Ines and Singh, S and Vidana-Villa, E and Grout, E and Morford, J and Emmerson, M and Jensens, F and Whitehead, H and Kiskin, Ivan and Strandburg-Peshkin, A and others},
  journal={arXiv preprint arXiv:2207.07911},
  year={2022}
}
The dataset is available at the following link:
https://zenodo.org/record/6517414/
'''
MIN_DURATION = 1. #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 1.
TAIL = 0.5 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.2 #seconds - add a front to the audio files to avoid cutting the beginning of the sound



class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='dcase_few_shot', *args, **kwargs):
        self.path = path
        process = dcase_few_shot_noise.Dataset.__dict__["process"]
        self.process_file = dcase_few_shot_noise.Dataset.__dict__["process_file"]
        #generate dataset if not already done
        process(self, conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)



# Links to the audio files
REMOTES = {
    "dev": download.RemoteFileMetadata(
        filename="Development_Set.zip",
        url="https://zenodo.org/record/6482837/files/Development_Set.zip?download=1",
        checksum="cf4d3540c6c78ac2b3df2026c4f1f7ea",
    ),
    "train-classes": download.RemoteFileMetadata(
        filename="DCASE2022_task5_Training_set_classes.csv",
        url="https://zenodo.org/record/6482837/files/DCASE2022_task5_Training_set_classes.csv?download=1",
        checksum="abce1818ba10436971bad0b6a3464aa6",
    ),
    "validation-classes": download.RemoteFileMetadata(
        filename="DCASE2022_task5_Validation_set_classes.csv",
        url="https://zenodo.org/record/6482837/files/DCASE2022_task5_Validation_set_classes.csv?download=1",
        checksum="0c05ff0c9e1662ff8958c4c812abffdb",
    ),
    "eval": download.RemoteFileMetadata(
        filename="Evaluation_set_5shots.zip",
        url="https://zenodo.org/record/6517414/files/Evaluation_set_5shots.zip?download=1",
        checksum="5212c0e133874bba1ee25c81ced0de99",
        destination_dir="Evaluation_Set"
    ),
}



