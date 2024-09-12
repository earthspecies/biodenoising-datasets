import torch
import torchaudio
import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
This is a private ESP dataset containing dolphins signature whistles.
'''

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='dolphins_signature_whistles', *args, **kwargs):
        self.path = path
        source_path = os.path.join(self.path,'audio')
        os.makedirs(source_path, exist_ok=True)
        anno = pd.read_pickle(os.path.join(self.path,'signature_whistles.pkl'))
        for (idx, row) in anno.iterrows():
            torchaudio.save(os.path.join(source_path,row.identity+'_'+str(idx)+'.wav'),torch.from_numpy(row.audio)[None,:], row.sample_rate)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "pkl": 
        download.RemoteFileMetadata(
            filename="signature_whistles.pkl",
            url="gs://dolphin_signature_whistles/signature_whistles.pkl",
            checksum="404c094776444334a8129d417c1ec083",
        ),
}
