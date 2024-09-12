import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public subset of underwater noises from the MARS MBARI project.
For more information, please check the website: https://www.mbari.org/project/open-acoustic-data/ 
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='marsmbari_noise', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        files = [f for f in os.listdir(self.path) if f.endswith('.wav')]
        for f in files:
            caption = "underwater noise"
            caption2 =  ''
            url= 's3://pacific-sound-256khz-2018'
            source = 'MARS MBARI'
            recordist = ''
            species_common = '' 
            species_scientific = ''
            audiocap_id = ''
            youtube_id = ''
            start_time = 0
            medium = 'underwater'
            species = ''
            relative_path = f
            row = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
            self.df.loc[len(self.df)] = row
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "MARS_20180331_235914": 
        download.RemoteFileMetadata(
            filename="MARS_20180331_235914.wav",
            url="s3://pacific-sound-256khz-2018/03/MARS_20180331_235914.wav",
            checksum="7aa91b3e0b7f5d884a7b8fe05ab35bc0",
        ),
    "MARS_20180131_230212": 
        download.RemoteFileMetadata(
            filename="MARS_20180131_230212.wav",
            url="s3://pacific-sound-256khz-2018/01/MARS_20180131_230212.wav",
            checksum="6208c4caaf2cbb43740c4576974c9851",
        ),
    "MARS_20180531_235913": 
        download.RemoteFileMetadata(
            filename="MARS_20180531_235913.wav",
            url="s3://pacific-sound-256khz-2018/05/MARS_20180531_235913.wav",
            checksum="3aa7f7fd3ec5bbd0a68bcf55861d2fdd",
        )
}

