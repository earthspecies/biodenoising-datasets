'''
This is a public dataset for benchmarking Neotropical anuran calls identification in passive acoustic monitoring.
For more information check the paper:
@article{canas2023dataset,
  title={A dataset for benchmarking Neotropical anuran calls identification in passive acoustic monitoring},
  author={Ca{\~n}as, Juan Sebasti{\'a}n and Toro-G{\'o}mez, Mar{\'\i}a Paula and Sugai, Larissa Sayuri Moreira and Ben{\'\i}tez Restrepo, Hern{\'a}n Dar{\'\i}o and Rudas, Jorge and Posso Bautista, Breyner and Toledo, Lu{\'\i}s Felipe and Dena, Simone and Domingos, Ad{\~a}o Henrique Rosa and de Souza, Franco Leandro and others},
  journal={Scientific Data},
  volume={10},
  number={1},
  pages={771},
  year={2023},
  publisher={Nature Publishing Group UK London}
}
'''
import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='anuraset', *args, **kwargs):
        self.path = path
        # sample_name,fname,min_t,max_t,site,date,species_number,subset,SPHSUR,BOABIS,
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="anuraset.zip",
        url="https://zenodo.org/records/8342596/files/anuraset.zip?download=1",
        checksum="7950ac82e288113c102b2a7ffa05b9dc",
    ),
}



