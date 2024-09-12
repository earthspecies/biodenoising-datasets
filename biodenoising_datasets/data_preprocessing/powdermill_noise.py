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
@dataset{chronister_2021_4656848,
  author       = {Chronister, Lauren M. and
                  Rhinehart, Tessa A. and
                  Place, Aidan and
                  Kitzes, Justin},
  title        = {{An annotated set of audio recordings of Eastern 
                   North American birds containing frequency, time,
                   and species information}},
  month        = apr,
  year         = 2021,
  publisher    = {Zenodo},
  doi          = {10.5061/dryad.d2547d81z},
  url          = {https://doi.org/10.5061/dryad.d2547d81z}
}
'''
DIRS = ['Recording_1','Recording_2','Recording_3','Recording_4']

MIN_DURATION_NOISE = 4.
MIN_DURATION = 0.5 #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 0.5
TAIL = 0.3 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='powdermill', *args, **kwargs):
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
            for d in DIRS:
                files = [os.path.join(self.path, d, f) for f in os.listdir(os.path.join(self.path,d)) if os.path.isfile(os.path.join(self.path,d, f)) and f.endswith(tuple(['.wav','.WAV'])) and not f.startswith('.')]
                for f in files:
                    self.process_file(f=f, data_path=self.path)
            

    def process_file(self, f, data_path, min_duration=8):
        path = f
        df = pd.read_csv(path[:-3]+'Table.1.selections.txt', sep='\t')
        ### loading audio
        audio, sr = torchaudio.load(path)
        
        # ### join events close apart in time
        # df.reset_index(drop=True, inplace=True)
        # if len(df)>1:
        #     index = 1
        #     while index < len(df):
        #         #print('{}->{}',format(df.iloc[index-1]['End Time (s)']),df.at[index,'Begin Time (s)'])
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
        if len(df) == 0:
            torchaudio.save(os.path.join(noise_path,os.path.basename(f)).replace(".WAV",".wav"), audio, sr)
        else:
            ### saving audio
            start_noise = 0
            for index, row in df.iterrows():
                # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Begin Time (s)"]+row["File Offset (s)"],row["End Time (s)"]+row["File Offset (s)"]))
                start = np.maximum(0,int(row["Begin Time (s)"]*sr) - int(FRONT*sr))
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
                    torchaudio.save(os.path.join(source_path,os.path.basename(f).replace(".WAV","_{}.wav".format(index)).replace(".wav","_{}.wav".format(index))), audio_source, sr)
                    # write the noise occurring before the event
                    # print("Noise {} Duration: {} {} {}".format(index, end_noise/sr-start_noise/sr,start_noise/sr,end_noise/sr))
                    if end_noise>start_noise and end_noise-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
                        self.slice_noise(audio_noise, sr, index, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, False)
                    start_noise = end
            # #write the remaining noise
            # # print("Duration: {}, {}-{}".format(audio.shape[1]/sr-start_noise/sr,start_noise/sr,audio.shape[1]/sr))
            if start_noise<audio.shape[1] and audio.shape[1]-start_noise>MIN_DURATION*sr and len(audio_noise.shape)==2:
                audio_noise = audio[:,start_noise:]
                self.slice_noise(audio_noise, sr, index+1, noise_path, f, MIN_DURATION, MIN_DURATION_NOISE, False)


# Links to the audio files
REMOTES = {
    "soundscape": download.RemoteFileMetadata(
        filename="wav_Files.zip",
        url="https://zenodo.org/record/4656848/files/wav_Files.zip?download=1s",
        checksum="2876c0cfc6ace1845ac04814ea9180f1",
    ),
    "annotations": download.RemoteFileMetadata(
        filename="annotation_Files.zip",
        url="https://zenodo.org/record/4656848/files/annotation_Files.zip?download=1",
        checksum="8f78ba7cf9fc5d25656f7747ed3406d1",
    ),
}



