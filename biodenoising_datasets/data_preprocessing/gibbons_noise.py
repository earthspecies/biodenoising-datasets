import os
from . import download
from .AudioDataset import AudioDataset
import pandas as pd 
import numpy as np 
import torchaudio
import utils
''' 
This is a public dataset of gibbons vocalizations.
For more info check the paper:
@article{jeantet2023improving,
  title={Improving deep learning acoustic classifiers with contextual information for wildlife monitoring},
  author={Jeantet, Lorene and Dufourq, Emmanuel},
  journal={Ecological Informatics},
  volume={77},
  pages={102256},
  year={2023},
  publisher={Elsevier}
}
'''
MIN_DURATION_NOISE = 4.
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='gibbons_noise', *args, **kwargs):
        self.path = path
        
        #generate dataset if not already done
        self.process(conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_noise')} if not hasattr(self, 'all_dirs') else self.all_dirs
        self.splits = ['all'] if not hasattr(self, 'splits') else self.splits
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    def process(self, conf, dname):
        audio_noise = os.path.join(self.path,'audio_noise')
        audio_source = os.path.join(self.path,'audio_source')
        if os.path.exists(audio_source):
            file_list = [f for f in os.listdir(audio_source) if os.path.isfile(os.path.join(audio_source, f)) and f.endswith('.wav') and not f.startswith('.')]
        else:
            file_list = []
        if len(file_list)<100:
            print("No audio files found in {}. Creating dataset.".format(audio_noise))
            os.makedirs(audio_noise, exist_ok=True)
            os.makedirs(audio_source, exist_ok=True)
            df = pd.read_csv(os.path.join(self.path,'annotations.csv'), sep=',')
            files = df["Filename"].unique()
            for f in files:
                df_file = df[df["Filename"]==f]
                self.process_file(f=f, df=df_file, data_path=self.path)
            
    def process(self, conf, dname):
        audio_noise = os.path.join(self.path,'audio_noise')
        audio_source = os.path.join(self.path,'audio_source')
        if os.path.exists(audio_source):
            file_list = [f for f in os.listdir(audio_source) if os.path.isfile(os.path.join(audio_source, f)) and f.endswith('.wav') and not f.startswith('.')]
        else:
            file_list = []
        
        if len(file_list)<10:
            print("No audio files found in {}. Creating dataset.".format(audio_noise))
            # os.makedirs(audio_noise, exist_ok=True)
            os.makedirs(audio_source, exist_ok=True)
            
            files = [f for f in os.listdir(os.path.join(self.path)) if os.path.isfile(os.path.join(self.path, f)) and f.endswith('.wav') and not f.startswith('.')]
            
            for f in files:
                parameters, frames, durations, labels, values = utils.svl.extractSvlAnnotRegionFile(os.path.join(self.path,'Annotations',f.replace('.wav','.svl')))
                #df_file = pd.read_xml(os.path.join(self.path,'Annotations',f.replace('.wav','.svl')))
                df_file = pd.DataFrame(columns=['Start Time (s)','Duration (s)', 'Label'])
                df_file['Start Time (s)'] = frames
                df_file['Duration (s)'] = durations
                df_file['Label'] = labels
                self.process_file(f=f, df_file=df_file, data_path=self.path)
            

    def process_file(self, f, df_file, data_path, min_duration=8):
        path = os.path.join(data_path,f)
        ### loading audio
        audio, sr = torchaudio.load(path)

        ### saving audio
        noise_condition = df_file["Label"]=='no-gibbon'
        for l, df in {"audio_source":df_file[~noise_condition]}.items(): #"audio_noise":df_file[noise_condition],
            for index, row in df.iterrows():
                # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Start Time (s)"]+row["File Offset (s)"],row["End Time (s)"]+row["File Offset (s)"]))
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
            
                    audio_chunk = audio[:,start:end]
                    torchaudio.save(os.path.join(data_path,l,f.replace(".wav","_{}.wav".format(index))), audio_chunk, sr)
        

# Links to the audio files
REMOTES = {
    "annotations": download.RemoteFileMetadata(
        filename="Annotations.zip",
        url="https://zenodo.org/record/7997739/files/Annotations.zip?download=1",
        checksum="edc5fd17c860d9bbafc8895a90da28fd",
    ),
    "audio1": download.RemoteFileMetadata(
        filename="Audio_1.zip",
        url="https://zenodo.org/record/7997739/files/Audio_1.zip?download=1",
        checksum="348936dbac82e46651eb703ac0f1223d",
    ),
    "audio2": download.RemoteFileMetadata(
        filename="Audio_2.zip",
        url="https://zenodo.org/record/7997739/files/Audio_2.zip?download=1",
        checksum="54bf496b776a612d206d8bd5a6f692ac",
    ),
    "audio3": download.RemoteFileMetadata(
        filename="Audio_3.zip",
        url="https://zenodo.org/record/7997739/files/Audio_3.zip?download=1",
        checksum="264c67854af78a2aa99a58d830960500",
    ),
    "audio4": download.RemoteFileMetadata(
        filename="Audio_4.zip",
        url="https://zenodo.org/record/7997739/files/Audio_4.zip?download=1",
        checksum="4a3ff80d3f13b3c47e218a5c0a15a419",
    )
}




