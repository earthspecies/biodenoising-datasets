import os
from . import south_alaskan_humpback_whales_noise
from . import download
from .AudioDataset import AudioDataset
''' 
This is a private ESP dataset containing humpback whale vocalizations.
For more information, please access the following paper:
@article{fournet2018more,
  title={More of the same: Allopatric humpback whale populations share acoustic repertoire},
  author={Fournet, Michelle EH and Jacobsen, Lauren and Gabriele, Christine M and Mellinger, David K and Klinck, Holger},
  journal={PeerJ},
  volume={6},
  pages={e5365},
  year={2018},
  publisher={PeerJ Inc.}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='south_alaskan_humpback_whales', *args, **kwargs):
        self.path = path
        process = south_alaskan_humpback_whales_noise.Dataset.__dict__["process"]
        self.process_file = south_alaskan_humpback_whales_noise.Dataset.__dict__["process_file"]
        process(self,conf, dname)
        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

REMOTES = {
    "full": 
        download.RemoteFileMetadata(
            filename="south_alaskan_humpback_whales_raw.zip",
            url="gs://south_alaskan_humpback_whales/south_alaskan_humpback_whales_raw.zip",
            checksum="d2a3c39095825c6b962034904bf08642",
        ),
}