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
This is a public dataset for bird call detection.
For more information, please access the following paper:
@dataset{stefan_kahl_2022_7050014,
  author       = {Stefan Kahl and
                  Connor M. Wood and
                  Philip Chaon and
                  M. Zachariah Peery and
                  Holger Klinck},
  title        = {{A collection of fully-annotated soundscape 
                   recordings from the Western United States}},
  month        = sep,
  year         = 2022,
  publisher    = {Zenodo},
  version      = 1,
  doi          = {10.5281/zenodo.7050014},
  url          = {https://doi.org/10.5281/zenodo.7050014}
}
'''
MIN_DURATION_NOISE = 4.
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound


class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='sierra_nevada_noise', *args, **kwargs):
        self.path = path
        self.activity_detector = utils.pcen.ActivityDetector()
        
        #generate dataset if not already done
        self.process(conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_noise')}
        self.splits = ['all']
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
            

    def process_file(self, f, df, data_path, min_duration=8):
        path = os.path.join(data_path,f)
        ### loading audio
        audio, sr = torchaudio.load(path)
        
        # ### join events close apart in time
        # df.reset_index(drop=True, inplace=True)
        # if len(df)>1:
        #     index = 1
        #     while index < len(df):
        #         #print('{}->{}',format(df.iloc[index-1]['End Time (s)']),df.at[index,'Start Time (s)'])
        #         if df.at[index,'start_time_s'] - (df.iloc[index-1]['start_time_s'] + df.iloc[index-1]['duration_s'])< MIN_INTERVAL:
        #             df.at[index-1,'duration_s'] = df.at[index,'start_time_s'] + df.at[index,'duration_s'] - df.iloc[index-1]['start_time_s']
        #             df.drop(index, inplace=True)
        #             df.reset_index(drop=True, inplace=True)
        #             #print(len(df))
        #         else:
        #             index += 1


        #import pdb;pdb.set_trace()
        path = os.path.join(data_path,'audio',f)
        noise_path = os.path.join(data_path,'audio_noise')
        source_path = os.path.join(data_path,'audio_source')
        # print("Processing file {}, Length {}".format(f, audio.shape[1]/sr))
        ### saving audio
        start_noise = 0
        for index, row in df.iterrows():
            # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Start Time (s)"]+row["File Offset (s)"],row["End Time (s)"]+row["File Offset (s)"]))
            start = np.maximum(0,int(row["Start Time (s)"]*sr) - int(FRONT*sr))
            end = int((row["End Time (s)"]-FRONT)*sr) + int(TAIL*sr)
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
                torchaudio.save(os.path.join(source_path,f.replace(".flac","_{}.wav".format(index))), audio_source, sr)
                # write the noise occurring before the event
                # print("Noise {} Duration: {} {} {}".format(index, end_noise/sr-start_noise/sr,start_noise/sr,end_noise/sr))
                if end_noise>start_noise and end_noise-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
                    self.slice_noise(audio_noise, sr, index, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, True)
                start_noise = end
        # #write the remaining noise
        # # print("Duration: {}, {}-{}".format(audio.shape[1]/sr-start_noise/sr,start_noise/sr,audio.shape[1]/sr))
        if start_noise<audio.shape[1] and audio.shape[1]-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
            audio_noise = audio[:,start_noise:]
            self.slice_noise(audio_noise, sr, index+1, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, True)

# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="soundscape_data.zip",
        url="https://zenodo.org/record/7050014/files/soundscape_data.zip?download=1",
        checksum="2874bdb56f18002a0e5b6fe2402b3c0b",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotations.csv",
        url="https://zenodo.org/record/7050014/files/annotations.csv?download=1",
        checksum="36adcb398a1b82d9b165d62f09d31b31",
    ),
}



