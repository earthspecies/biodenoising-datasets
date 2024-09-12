'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
import pandas as pd 
import numpy as np 
import torchaudio
import utils
'''
This is a public dataset containg lemur vocalizations.
For more information, please refer to the following paper:
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
    def __init__(self, conf, path, dname='lemur_noise', *args, **kwargs):
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
            
            for s in [1,3]:
                subset = str(s)
                files = [f for f in os.listdir(os.path.join(self.path, 'Audio'+subset)) if os.path.isfile(os.path.join(self.path,  'Audio'+subset, f)) and f.endswith('.wav') and not f.startswith('.')]
                
                for f in files:
                    parameters, frames, durations, labels, values = utils.svl.extractSvlAnnotRegionFile(os.path.join(self.path, 'Annotations'+subset,f.replace('.wav','.svl')))
                    #df_file = pd.read_xml(os.path.join(self.path,'Annotations',f.replace('.wav','.svl')))
                    df_file = pd.DataFrame(columns=['Start Time (s)','Duration (s)', 'Label'])
                    df_file['Start Time (s)'] = frames
                    df_file['Duration (s)'] = durations
                    df_file['Label'] = labels
                    self.process_file(f=f, df_file=df_file, data_path=self.path, subset=subset)
            

    def process_file(self, f, df_file, data_path, subset, min_duration=8):
        path = os.path.join(data_path,  'Audio'+subset, f)
        ### loading audio
        audio, sr = torchaudio.load(path)

        ### saving audio
        source_condition = df_file["Label"]=='roar'
        for l, df in {"audio_source":df_file[source_condition]}.items(): #"audio_noise":df_file[noise_condition],
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
    "annotations1": download.RemoteFileMetadata(
        filename="Annotations1.zip",
        url="https://zenodo.org/record/6331594/files/Annotations1.zip?download=1",
        checksum="1a4f202beec54e2892d0f762d96ce613",
    ),
    "annotations2": download.RemoteFileMetadata(
        filename="Annotations2.zip",
        url="https://zenodo.org/record/6331594/files/Annotations2.zip?download=1",
        checksum="7637e2b3934c5cf56ef1431f15ae6440",
    ),
    "annotations3": download.RemoteFileMetadata(
        filename="Annotations3.zip",
        url="https://zenodo.org/record/6331594/files/Annotations3.zip?download=1",
        checksum="3de9d2350b7bc791d6783dcd268cd608",
    ),
    "audio1": download.RemoteFileMetadata(
        filename="Audio1.zip",
        url="https://zenodo.org/record/6331594/files/Audio1.zip?download=1",
        checksum="d5759942065acc1cb02d662ad33c4885",
    ),
    "audio2": download.RemoteFileMetadata(
        filename="Audio2.zip",
        url="https://zenodo.org/record/6331594/files/Audio2.zip?download=1",
        checksum="6d52bd36f9e0c0b35cf8c10bef67ca33",
    ),
    "audio3": download.RemoteFileMetadata(
        filename="Audio3.zip",
        url="https://zenodo.org/record/6331594/files/Audio3.zip?download=1",
        checksum="8c3b10dec6c54a36f5016440ceb3efd8",
    )
}




