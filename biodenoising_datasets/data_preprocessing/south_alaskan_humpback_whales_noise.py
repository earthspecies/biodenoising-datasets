import os
import torch
import pandas as pd
import torchaudio
import scipy
import numpy as np
from . import download
from .AudioDataset import AudioDataset
''' 
This is a private ESP dataset containing humpback whale vocalizations.
For more information, please access the following paper:
@article{fournet2018more,
  title={More of the same: Allopatric humpback whale populations share acoustic repertoire},
  author={Fournet, Michelle EH and Jacobsen, Lauren and Gabriele, Christine M and Mellinger, David K and Klinck, Holger},
  journal={PeerJ},
  volume={6},
  pages={e5365},
  year={2018},
  publisher={PeerJ Inc.}
}
'''
GAIN = 30.
NOISE_BLACKLIST = ['190806140351.wav','190806140551.wav','190806140751.wav','190806141151.wav']
MIN_DURATION = 2 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.2 #seconds - add a tail to the audio files to avoid cutting the end of the whale sound
FRONT = 0.05 #seconds - add a front to the audio files to avoid cutting the beginning of the whale sound

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='south_alaskan_humpback_whales_noise', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        
        #generate dataset if not already done
        self.process(conf, dname)

        self.all_dirs = {'all':os.path.join(self.path,'audio_noise')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

    def process(self, conf, dname):
        audio_noise = os.path.join(self.path,'audio_noise')
        audio_source = os.path.join(self.path,'audio_source')
        if os.path.exists(audio_noise):
            file_list = [f for f in os.listdir(audio_noise) if os.path.isfile(os.path.join(audio_noise, f)) and f.endswith('.wav') and not f.startswith('.')]
        else:
            file_list = []
        
        if len(file_list)<100:
            print("No audio files found in {}. Creating dataset.".format(audio_noise))
            os.makedirs(audio_noise, exist_ok=True)
            os.makedirs(audio_source, exist_ok=True)
            df = pd.read_csv(os.path.join(self.path,'selection_tables.txt'), sep='\t')
            df["Begin File"] = df["Begin File"].apply(lambda x: x.replace("__+25dB", ""))
            files = df["Begin File"].unique()
            for f in files:
                df_file = df[df["Begin File"]==f]
                self.process_file(self, f=f, df=df_file, data_path=self.path)
            

    def process_file(self, f, df, data_path, min_duration=8):
        path = os.path.join(data_path,'audio',f)
        ### loading audio
        audio, sr = torchaudio.load(path)

        lowcut=1 #Hz - remove the dc component without affecting the low frequencies of whale sounds
        [b,a] = scipy.signal.butter(4,lowcut, fs=sr, btype='high')
        audio = torch.from_numpy(scipy.signal.lfilter(b,a,audio.numpy())).type(torch.float32)
        
        ### join events close apart in time
        df.reset_index(drop=True, inplace=True)
        if len(df)>1:
            index = 1
            while index < len(df):
                #print('{}->{}',format(df.iloc[index-1]['End Time (s)']),df.at[index,'Begin Time (s)'])
                if df.at[index,'Begin Time (s)'] - df.iloc[index-1]['End Time (s)'] < MIN_INTERVAL:
                    df.at[index-1,'End Time (s)'] = df.at[index,'End Time (s)']
                    df.drop(index, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    #print(len(df))
                else:
                    index += 1


        path = os.path.join(data_path,'audio',f)
        noise_path = os.path.join(data_path,'audio_noise')
        source_path = os.path.join(data_path,'audio_source')
        # print("Processing file {}, Length {}".format(f, audio.shape[1]/sr))
        ### saving audio
        start_noise = 0
        for index, row in df.iterrows():
            # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Begin Time (s)"]+row["File Offset (s)"],row["End Time (s)"]+row["File Offset (s)"]))
            start = np.maximum(0,int(row["File Offset (s)"]*sr) - int(FRONT*sr))
            end = int((row["End Time (s)"]-row["Begin Time (s)"]+row["File Offset (s)"]-FRONT)*sr) + int(TAIL*sr)
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
                audio_source = GAIN*audio[:,start:end]
                audio_noise = GAIN*audio[:,start_noise:end_noise]
                channel_source = int(row["Channel"])-1
                # import pdb;pdb.set_trace()
                torchaudio.save(os.path.join(source_path,f.replace(".wav","_{}.wav".format(index))), audio_source[None,channel_source,:], sr)
                #write the noise occuring before the event
                # print("Noise {} Duration: {} {} {}".format(index, end_noise/sr-start_noise/sr,start_noise/sr,end_noise/sr))
                if end_noise>start_noise and end_noise-start_noise>MIN_DURATION*sr and f not in NOISE_BLACKLIST:
                    for ch in range(4):
                        torchaudio.save(os.path.join(noise_path,f.replace(".wav","_{}_{}.wav".format(index,ch))), audio_noise[None,ch,:], sr)
                start_noise = end
        #write the remaining noise
        # print("Duration: {}, {}-{}".format(audio.shape[1]/sr-start_noise/sr,start_noise/sr,audio.shape[1]/sr))
        if start_noise<audio.shape[1] and audio.shape[1]-start_noise>MIN_DURATION*sr and f not in NOISE_BLACKLIST:
            audio_noise = audio[:,start_noise:]
            for ch in range(4):
                torchaudio.save(os.path.join(noise_path,f.replace(".wav","_{}_{}.wav".format(index+1,ch))), audio_noise[None,ch,:], sr)
            



REMOTES = {
    "full": 
        download.RemoteFileMetadata(
            filename="south_alaskan_humpback_whales_raw.zip",
            url="gs://south_alaskan_humpback_whales/south_alaskan_humpback_whales_raw.zip",
            checksum="d2a3c39095825c6b962034904bf08642",
        ),
}