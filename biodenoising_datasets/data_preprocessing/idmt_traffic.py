import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
This is a public domain dataset for acoustic traffic monitoring research.
@inproceedings{abesser2021idmt,
  title={IDMT-traffic: an open benchmark dataset for acoustic traffic monitoring research},
  author={Abe{\ss}er, Jakob and Gourishetti, Saichand and K{\'a}tai, Andr{\'a}s and Clau{\ss}, Tobias and Sharma, Prachi and Liebetrau, Judith},
  booktitle={2021 29th European Signal Processing Conference (EUSIPCO)},
  pages={551--555},
  year={2021},
  organization={IEEE}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='idmt_traffic', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        files = [f for f in os.listdir(os.path.join(self.path, 'IDMT_Traffic', 'audio')) if f.endswith('.wav')]
        for f in files:
            caption = 'car'
            caption2 = 'street'
            url= 'https://zenodo.org/record/7551553'
            source = 'IDMT_Traffic'
            recordist = ''
            species_common = ''
            species_scientific = ''
            audiocap_id = ''
            youtube_id = ''
            medium = 'terrestrial'
            start_time = 0
            species = ''
            relative_path = os.path.join('IDMT_Traffic','audio', f)
            rowdf = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
            self.df.loc[len(self.df)] = rowdf
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "zip": download.RemoteFileMetadata(
        filename="IDMT_Traffic.zip",
        url="https://zenodo.org/record/7551553/files/IDMT_Traffic.zip?download=1",
        checksum="7ca2311ca32203aec5074a5fe933e343",
    ),
}



