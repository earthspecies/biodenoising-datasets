'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
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

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='dcase_few_shot_eval', *args, **kwargs):
        self.path = path

        self.all_dirs = {'HT':os.path.join(self.path,'Development_Set','Training_Set','HT'),'QU':os.path.join(self.path,'Evaluation_Set','QU')}
        self.splits = ['HT','QU']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)



# Links to the audio files
REMOTES = {
    "eval": download.RemoteFileMetadata(
        filename="Evaluation_set_5shots.zip",
        url="https://zenodo.org/record/6517414/files/Evaluation_set_5shots.zip?download=1",
        checksum="5212c0e133874bba1ee25c81ced0de99",
        destination_dir="Evaluation_Set"
    ),
}



