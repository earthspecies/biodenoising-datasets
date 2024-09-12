'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
import pandas as pd 
import numpy as np 
import torchaudio
#torchaudio._extension._init_ffmpeg()
import utils
import librosa
import torch
''' 
This is a public subset of xeno-canto dataset containing detection labels for bird songs.
For more information, please access the following paper:
@dataset{jeantet_lorene_2023_7828148,
  author       = {Jeantet Lorene and
                  Dufourq Emmanuel},
  title        = {{Manually labeled Bird song dataset of 22 species 
                   from Xeno-canto to enhance deep learning acoustic
                   classifiers with contextual information.}},
  month        = apr,
  year         = 2023,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.7828148},
  url          = {https://doi.org/10.5281/zenodo.7828148}
}
'''
MIN_DURATION_NOISE = 4.
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound

birds_dict = {
    'Paridae Saxicola rubetra': 'Whinchat',
    'Turdidae Catharus aurantiirostris': 'Orange-billed Nightingale-Thrush',
    'Troglodytidae Troglodytes aedon': 'House Wren',
    'Paridae Hypocnemis hypoxantha': 'Yellow-browed Antbird',
    'Paridae Hypocnemis cantator': 'Warbling Antbird',
    'Fringillidae Serinus serinus': 'European Serin',
    'Turdidae Catharus fuscater': 'Slaty-backed Nightingale-Thrush',
    'Turdidae Catharus ustulatus': 'Swainson\'s Thrush',
    'Paridae Saxicola rubicola': 'European Stonechat',
    'Troglodytidae Troglodytes pacificus': 'Pacific Wren',
    'Turdidae Catharus fuscescens': 'Veery',
    'Troglodytidae Troglodytes hiemalis': 'Winter Wren',
    'Fringillidae Serinus canicollis': 'Cape Canary',
    'Fringillidae Serinus icollis': 'Yellow-fronted Canary',
    'Troglodytidae Troglodytes troglodytes': 'Eurasian Wren',
    'Turdidae Catharus guttatus': 'Hermit Thrush',
    'Paridae Hypocnemis striata': 'Stripe-breasted Antbird',
    'Turdidae Catharus bicknelli': 'Bicknell\'s Thrush',
    'Turdidae Catharus minimus': 'Gray-cheeked Thrush',
    'Paridae Saxicola tectes': 'Réunion Stonechat',
    'Paridae Saxicola rubicola': 'European Stonechat',
    'Paridae Hypocnemis peruviana': 'Peruvian Warbling Antbird',
    'Paridae Saxicola rubetra': 'Whinchat',
    'Paridae Saxicola torquatus': 'African Stonechat',
    'Paridae Saxicola gutturalis': 'White-throated Bush Chat',
    'Troglodytidae Troglodytes troglodytes': 'Eurasian Wren',
    'Turdidae Catharus aurantiirostris ': 'Orange-billed Nightingale-Thrush',
}


class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='xeno_canto_labeled_noise', *args, **kwargs):
        self.path = path
        self.all_species={}
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        #generate dataset if not already done
        self.process(conf, dname)
        self.all_dirs = {'all':os.path.join(self.path,'audio_noise')} if not hasattr(self, 'all_dirs') else self.all_dirs
        self.splits = ['all'] if not hasattr(self, 'splits') else self.splits
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    def process(self, conf, dname):
        audio_noise = os.path.join(self.path,'audio_noise')
        audio_source = os.path.join(self.path,'audio_source')

        print("Creating dataset.".format(audio_noise))
        os.makedirs(audio_noise, exist_ok=True)
        os.makedirs(audio_source, exist_ok=True)
        
        for subset in ['Training','Validation']:
            files = [f for f in os.listdir(os.path.join(self.path, subset)) if os.path.isfile(os.path.join(self.path, subset, f)) and f.endswith('.mp3') and not f.startswith('.')]
            for f in files:
                parameters, frames, durations, labels, values = utils.svl.extractSvlAnnotRegionFile(os.path.join(self.path,subset,f.replace('.mp3','.svl')))
                #df_file = pd.read_xml(os.path.join(self.path,'Annotations',f.replace('.wav','.svl')))
                df_file = pd.DataFrame(columns=['Start Time (s)','Duration (s)', 'Label'])
                df_file['Start Time (s)'] = frames
                df_file['Duration (s)'] = durations
                df_file['Label'] = labels
                self.process_file(f=f, df_file=df_file, data_path=self.path, subset=subset)
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)

    def process_file(self, f, df_file, data_path, subset, min_duration=8):
        path = os.path.join(data_path, subset, f)
        ### loading audio
        try:
            audio, sr = torchaudio.load(path, normalize=True)
            audio = audio.float()
        except Exception as e:
            # audio, sr = sf.read(path)
            audio, sr = librosa.load(path, sr=None)
            audio = librosa.util.normalize(audio)
            audio = torch.from_numpy(audio).float()
            if len(audio.shape)==1:
                audio = audio.unsqueeze(0)
            
        noise_path = os.path.join(data_path,'audio_noise')
        source_path = os.path.join(data_path,'audio_source')

        ### saving audio
        start_noise = 0
        for index, row in df_file.iterrows():
            # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Begin Time (s)"]+row["File Offset (s)"],row["End Time (s)"]+row["File Offset (s)"]))
            start = np.maximum(0,int(row["Start Time (s)"]*sr) - int(FRONT*sr))
            end = int((row["Start Time (s)"]+row["Duration (s)"]-FRONT)*sr) + int(TAIL*sr)
            if start < end < audio.shape[1]:
                if end-start<MIN_DURATION*sr:
                    diff = int(MIN_DURATION*sr) - (end-start)
                    if start - diff/2 < 0:
                        start = 0
                        end = int(MIN_DURATION*sr)
                    elif end + diff/2 > audio.shape[1]:
                        end = audio.shape[1]
                        start = int(audio.shape[1] - MIN_DURATION*sr)
                    else:
                        start = int(start - diff/2)
                        end = int(end + diff/2)
                # print("Source {} Duration: {}, {}-{}".format(index, end/sr-start/sr,start/sr,end/sr))
                    # if end/sr-start/sr < 0:
                    #     import pdb;pdb.set_trace()
                end_noise =  start
                audio_source = audio[:,start:end]
                audio_noise = audio[:,start_noise:end_noise]
                torchaudio.save(os.path.join(source_path,os.path.basename(f).replace(".mp3","_{}.wav".format(index))), audio_source, sr)
                # write the noise occurring before the event
                # print("Noise {} Duration: {} {} {}".format(index, end_noise/sr-start_noise/sr,start_noise/sr,end_noise/sr))
                # if end_noise>start_noise and end_noise-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
                #     self.slice_noise(audio_noise, sr, index, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, True)
                start_noise = end
                if len(row["Label"].split('_'))<2:
                    continue
                species1 = row["Label"].split('_')[0]
                species1 = species1.strip()
                species1 = species1.replace('aridae','Paridae') if species1.startswith('aridae') else species1
                species1 = species1.replace('ae','Paridae') if species1.startswith('ae') else species1
                species1 = species1.replace('idae','Paridae') if species1.startswith('idae') else species1
                species1 = species1.replace('oglodytidae','Troglodytidae') if species1.startswith('oglodytidae') else species1
                species1 = species1.replace('roglodytidae','Troglodytidae') if species1.startswith('roglodytidae') else species1
                species2 = row["Label"].split('_')[1]
                species3 = row["Label"].split('_')[2].split(',')[0].split('.')[0]
                caption = species1 + ' ' + species2 + ' ' + species3
                self.all_species[caption] = caption
                try:
                    caption2 =  birds_dict[caption]
                except:
                    import pdb;pdb.set_trace()
                caption2 =  birds_dict[caption]
                url= ''
                source = 'xeno-canto'
                recordist = ''
                species_common = birds_dict[caption]
                species_scientific = caption
                audiocap_id = ''
                youtube_id = ''
                start_time = 0
                medium = 'terrestrial'
                species = ''
                relative_path = os.path.join('audio_source',os.path.basename(f).replace(".mp3","_{}.wav".format(index)))
                row = {'dirs':subset,'medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                self.df.loc[len(self.df)] = row
        
        # 
        # #write the remaining noise
        # # print("Duration: {}, {}-{}".format(audio.shape[1]/sr-start_noise/sr,start_noise/sr,audio.shape[1]/sr))
        # if start_noise<audio.shape[1] and audio.shape[1]-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
        #     audio_noise = audio[:,start_noise:]
        #     self.slice_noise(audio_noise, sr, index+1, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, True)

# Links to the audio files
REMOTES = {
    "annotation": download.RemoteFileMetadata(
        filename="Annotation.zip",
        url="https://zenodo.org/record/7828148/files/Annotation.zip?download=1",
        checksum="31606f08b7001d93a4a7796dd77ae18e",
    ),
    "audio": download.RemoteFileMetadata(
        filename="Audio.zip",
        url="https://zenodo.org/record/7828148/files/Audio.zip?download=1",
        checksum="17260b6dbffb367dfaf57d609089cf75",
    ),
}




