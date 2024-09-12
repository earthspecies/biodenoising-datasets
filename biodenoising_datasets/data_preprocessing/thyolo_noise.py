import os
from . import download
from .AudioDataset import AudioDataset
import pandas as pd 
import numpy as np 
import torchaudio
import utils
'''
This is a public dataset containing thyolo calls.
For more information, please access the following paper:
@article{dufourq2022passive,
  title={Passive acoustic monitoring of animal populations with transfer learning},
  author={Dufourq, Emmanuel and Batist, Carly and Foquet, Ruben and Durbach, Ian},
  journal={Ecological Informatics},
  volume={70},
  pages={101688},
  year={2022},
  publisher={Elsevier}
}

'''
MIN_DURATION_NOISE = 4.
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='thyolo_noise', *args, **kwargs):
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
            os.makedirs(audio_noise, exist_ok=True)
            os.makedirs(audio_source, exist_ok=True)
            
            files = [f for f in os.listdir(os.path.join(self.path,'Audio')) if os.path.isfile(os.path.join(self.path,'Audio', f)) and f.endswith('.WAV') and not f.startswith('.')]
            
            for f in files:
                if os.path.exists(os.path.join(self.path,'Annotations',f.replace('.WAV','.svl'))):
                    parameters, frames, durations, labels, values = utils.svl.extractSvlAnnotRegionFile(os.path.join(self.path,'Annotations',f.replace('.WAV','.svl')))
                    #df_file = pd.read_xml(os.path.join(self.path,'Annotations',f.replace('.WAV','.svl')))
                    df_file = pd.DataFrame(columns=['Start Time (s)','Duration (s)', 'Label'])
                    df_file['Start Time (s)'] = frames
                    df_file['Duration (s)'] = durations
                    df_file['Label'] = labels
                    self.process_file(f=f, df_file=df_file, data_path=self.path)
            

    def process_file(self, f, df_file, data_path, min_duration=8):
        path = os.path.join(data_path,'Audio',f)
        ### loading audio
        audio, sr = torchaudio.load(path)

        ### saving audio
        noise_condition = df_file["Label"]=='noise'
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
                    torchaudio.save(os.path.join(data_path,l,f.replace(".WAV","_{}.wav".format(index))), audio_chunk, sr)
        

# Links to the audio files
REMOTES = {
    "annotations": download.RemoteFileMetadata(
        filename="Annotations.zip",
        url="https://zenodo.org/record/6328244/files/Annotations.zip?download=1",
        checksum="68a74edb724c90fd6010ff8e3ea8a4f9",
    ),
    "audio": download.RemoteFileMetadata(
        filename="Audio.zip",
        url="https://zenodo.org/record/6328244/files/Audio.zip?download=1",
        checksum="5ccf10e4de716a5f583eea591d49f220",
    ),
}




