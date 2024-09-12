import os
from . import download
from .AudioDataset import AudioDataset
''' 
These are some recordings from the NIPS4B dataset.
For more information, please access the following paper:
@article{glotin2013neural,
  title={Neural information processing scaled for bioacoustics, from neurons to big data},
  author={Glotin, H and LeCun, Y and Arti{\`e}res, T and Mallat, S and Tchernichovski, O and Halkias, X},
  journal={Proceedings of Neural Information Processing Scaled for Bioacoustics: from Neurons to Big Data},
  volume={2013},
  year={2013}
}
The dataset was described and downloaded from: https://sabiod.univ-tln.fr/nips4b/ . It may not be directly accessible from the internet.
'''

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='sabiod_samples', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "humpback": 
        download.RemoteFileMetadata(
            filename="NIPS4B_Humpback_Darewin_LaReunion_Jul_03_2013-001_26min.wav",
            #url="http://sabiod.univ-tln.fr/nips4b/media/NIPS4B_Humpback_Darewin_LaReunion_Jul_03_2013-001_26min.wav",
            url="gs://sabiod_data_samples/NIPS4B_Humpback_Darewin_LaReunion_Jul_03_2013-001_26min.wav",
            checksum="7e412265cee0705c452e87850b7a5539",
        ),
    "bombyx": 
        download.RemoteFileMetadata(
            filename="BOMBYX_SABIOD_UTLN_LSIS_PNPC_july2014_f412.wav",
            #url="http://sabiod.lis-lab.fr/media/BOMBYX_SABIOD_UTLN_LSIS_PNPC_july2014_f412.wav",
            url="gs://sabiod_data_samples/BOMBYX_SABIOD_UTLN_LSIS_PNPC_july2014_f412.wav",
            checksum="e9906909dc1244461c93668267917869",
        ),
    "tursiops": 
        download.RemoteFileMetadata(
            filename="Tursiops_truncatus_Nicky_SHARKD_0002S34D12_day3_aug2013_SABIOD_96kHz_32bits_after19min_nips4bfile_e.wav",
            #url="http://sabiod.lis-lab.fr/nips4b/media/Tursiops_truncatus_Nicky_SHARKD_0002S34D12_day3_aug2013_SABIOD_96kHz_32bits_after19min_nips4bfile_e.wav",
            url="gs://sabiod_data_samples/Tursiops_truncatus_Nicky_SHARKD_0002S34D12_day3_aug2013_SABIOD_96kHz_32bits_after19min_nips4bfile_e.wav",
            checksum="c8c260cd7a54f2e2139505abf88bb3d0",
        ),
}
