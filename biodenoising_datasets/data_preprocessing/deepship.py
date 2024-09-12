import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset

''' 
This is a public dataset for benchmarking ship sound classification.
For more information check the paper:
@article{irfan2021deepship,
  title={DeepShip: An underwater acoustic benchmark dataset and a separable convolution based autoencoder for classification},
  author={Irfan, Muhammad and Jiangbin, ZHENG and Ali, Shahid and Iqbal, Muhammad and Masood, Zafar and Hamid, Umar},
  journal={Expert Systems with Applications},
  volume={183},
  pages={115270},
  year={2021},
  publisher={Elsevier}
}
'''

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='deepship', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        folders = [f for f in os.listdir(os.path.join(self.path, 'DeepShip-main')) if os.path.isdir(os.path.join(self.path, 'DeepShip-main', f))]
        for d in folders:
            files = [f for f in os.listdir(os.path.join(self.path, 'DeepShip-main', d)) if f.endswith('.wav')]
            metafile = d.lower()+'-metafile'
            df = pd.read_csv(os.path.join(self.path, 'DeepShip-main', d, metafile), sep=',',names=['r1','r2','r3','r4','r5','r6','r7'])
            for f in files:
                fileid = int(f.split('.wav')[0])
                row = df.iloc[fileid-1]
                caption = d + ' boat'
                caption2 =  row['r2'].lower()
                url= 'https://github.com/irfankamboh/DeepShip'
                source = 'DeepShip'
                recordist = ''
                species_common = ''
                species_scientific = ''
                audiocap_id = ''
                youtube_id = ''
                start_time = 0
                medium = 'underwater'
                species = ''
                relative_path = os.path.join('DeepShip-main',d, f)
                rowdf = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                self.df.loc[len(self.df)] = rowdf
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "archive": download.RemoteFileMetadata(
        filename="main.zip",
        url="https://github.com/irfankamboh/DeepShip/archive/refs/heads/main.zip",
        checksum="b9dbf354cfb1d459dbf1ca8292209b00",
    )
}
