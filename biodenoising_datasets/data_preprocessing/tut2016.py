'''
'''
import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
''' 
This is a subset for the TUT2016 dataset, a public dataset containing sound events from the TUT-sound-events-2016-evaluation dataset.
For more information, please access the following paper:
@inproceedings{mesaros2016tut,
  title={TUT database for acoustic scene classification and sound event detection},
  author={Mesaros, Annamaria and Heittola, Toni and Virtanen, Tuomas},
  booktitle={2016 24th European Signal Processing Conference (EUSIPCO)},
  pages={1128--1132},
  year={2016},
  organization={IEEE}
}
'''
ALL_DIRS = ['home', 'residential_area']
DIRS = ['home'] 

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='tut2016', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        files = [f for f in os.listdir(os.path.join(self.path,'TUT-sound-events-2016-evaluation','audio','home') ) if f.endswith('.wav')]
        for f in files:
            caption = 'environmental noise'
            caption2 = ''
            url= 'https://zenodo.org/record/996424'
            source = 'TUT2016'
            recordist = ''
            species_common = ''
            species_scientific = ''
            audiocap_id = ''
            youtube_id = ''
            medium = 'terrestrial'
            start_time = 0
            species = ''
            relative_path = os.path.join('TUT-sound-events-2016-evaluation','audio','home', f)
            rowdf = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
            self.df.loc[len(self.df)] = rowdf
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="TUT-sound-events-2016-evaluation.audio.zip",
        url="https://zenodo.org/record/996424/files/TUT-sound-events-2016-evaluation.audio.zip?download=1",
        checksum="29434e8c53bd51206df0234e6cf2238c",
    ),
}



