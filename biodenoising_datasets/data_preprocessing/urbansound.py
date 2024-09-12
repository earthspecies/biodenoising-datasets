import os
import pandas as pd
import torch
import torchaudio
import librosa
from . import download
from .AudioDataset import AudioDataset, ALLOWED_EXTENSIONS
''' 
This is a subset of the UrbanSound dataset containing acoustic soundscapes from freesound.
For more information, please access the following paper:
@inproceedings{salamon2014dataset,
  title={A dataset and taxonomy for urban sound research},
  author={Salamon, Justin and Jacoby, Christopher and Bello, Juan Pablo},
  booktitle={Proceedings of the 22nd ACM international conference on Multimedia},
  pages={1041--1044},
  year={2014}
}
'''
# Global parameter
ALL_DIRS = ['air_conditioner', 'car_horn', 'children_playing', 'dog_bark', 'drilling', 'engine_idling', 'gun_shot', 'jackhammer', 'siren', 'street_music'] #,'FSD50K.dev_audio']
DIRS = ['air_conditioner', 'car_horn', 'drilling', 'engine_idling', 'jackhammer'] 
        
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='urbansound', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])

        #generate dataset if not already done
        self.process(conf, dname)
        self.all_dirs = {'all':os.path.join(self.path,'audio_noise')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    def process(self, conf, dname):
        audio_noise = os.path.join(self.path,'audio_noise')
        print("Creating dataset.".format(audio_noise))
        os.makedirs(audio_noise, exist_ok=True)
        # file_list = [os.path.join(root,file) for root,fdir,files in os.walk(self.path) for file in files if file.endswith(tuple(ALLOWED_EXTENSIONS)) and not file.startswith('.')]
        for d in DIRS:
            file_list = [os.path.join(self.path,'data',d,f) for f in os.listdir(os.path.join(self.path,'data',d)) if os.path.isfile(os.path.join(self.path,'data',d,f)) and f.endswith(tuple(ALLOWED_EXTENSIONS)) and not f.startswith('.')]
            for f in file_list:
                ext = f.split('.')[-1]
                df = pd.read_csv(f.replace(ext,'csv'), header=None, names=['start','end','id','label'])
                try:
                    audio, sr = torchaudio.load(f)
                except Exception as e:
                    audio, sr = librosa.load(f, sr=None)
                    audio = torch.from_numpy(audio)
                if len(audio.shape)>1:
                    audio = audio.sum(dim=0) 
                for i, row in df.iterrows():
                    chunk = audio[int(row['start']*sr):int(row['end']*sr)]
                    filename = os.path.join(audio_noise,os.path.basename(f).replace("."+ext,"_{}_{}.wav".format(row['label'],i)))
                    torchaudio.save(filename, chunk[None,...], sr)
                    caption = row['label']
                    caption2 = row['label']
                    url= 'https://urbansounddataset.weebly.com/'
                    source = 'Urbansound'
                    recordist = ''
                    species_common = ''
                    species_scientific = ''
                    audiocap_id = ''
                    youtube_id = ''
                    start_time = 0
                    medium = 'terrestrial'
                    species = ''
                    relative_path = os.path.join('audio_noise',os.path.basename(f).replace("."+ext,"_{}_{}.wav".format(row['label'],i)))
                    rowdf = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                    self.df.loc[len(self.df)] = rowdf

            
            

# Links to the audio files
REMOTES = {
    "Urbansound": 
        download.RemoteFileMetadata(
            filename="UrbanSound.tar.gz",
            url="https://zenodo.org/record/1206938/files/UrbanSound.tar.gz?download=1",
            checksum="b19549e1ad4799f9bb006a41d987aa56",
        )
}


