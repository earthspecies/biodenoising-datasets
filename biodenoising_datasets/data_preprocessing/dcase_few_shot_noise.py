import os
from . import download
from .AudioDataset import AudioDataset
import torchaudio
import numpy as np
import pandas as pd
import torch
'''
This is a public dataset for benchmarking few-shot bioacoustic event detection.
For more information check the paper:
@article{nolasco2022few,
  title={Few-shot bioacoustic event detection at the DCASE 2022 challenge},
  author={Nolasco, Ines and Singh, S and Vidana-Villa, E and Grout, E and Morford, J and Emmerson, M and Jensens, F and Whitehead, H and Kiskin, Ivan and Strandburg-Peshkin, A and others},
  journal={arXiv preprint arXiv:2207.07911},
  year={2022}
}
The dataset is available at the following link:
https://zenodo.org/record/6517414/
'''
MIN_DURATION = 1. #seconds - minimum duration of the audio files to be saved
MIN_INTERVAL = 1.
TAIL = 0.2 #seconds - add a tail to the audio files to avoid cutting the end of the sound
FRONT = 0.1 #seconds - add a front to the audio files to avoid cutting the beginning of the sound
MIN_DURATION_NOISE = 4.

DIRS_SOURCE = ['BV','PB','MT','JD','WMW']
DIRS_NOISE = ['BV','PB','MT']

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='dcase_few_shot_noise', *args, **kwargs):
        self.path = path
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
            dev_dir = os.path.join(self.path,'Development_Set')
            
            files = [os.path.join(root,file) for root,fdir,files in os.walk(dev_dir) for file in files if file.endswith('.wav') and not file.startswith('.')]
            for f in files:
                self.process_file(f=f, data_path=self.path)
            

    def process_file(self, f, data_path, min_duration=4):
        path = f
        class_label = os.path.basename(os.path.dirname(f))
        write_noise = True if class_label in DIRS_NOISE else False
        write_source = True if class_label in DIRS_SOURCE else False
        
        ### loading audio
        audio, sr = torchaudio.load(path)
        if os.path.exists(os.path.join(self.path,path[:-3]+'csv')):
            df = pd.read_csv(os.path.join(self.path,path[:-3]+'csv'), sep=',')
            class_columns = [col for col in df.columns if col not in ['Starttime','Endtime','Audiofilename']]
            df = df[(df[class_columns]=='POS').any(axis=1)]

            # import pdb; pdb.set_trace()
            ## join events close apart in time
            # df.reset_index(drop=True, inplace=True)
            # if len(df)>1:
            #     index = 1
            #     while index < len(df):
            #         #print('{}->{}',format(df.iloc[index-1]['Endtime']),df.at[index,'Starttime'])
            #         if df.at[index,'Starttime'] - df.iloc[index-1]['Endtime'] < MIN_INTERVAL:
            #             df.at[index-1,'Endtime'] = df.at[index,'Endtime']
            #             df.drop(index, inplace=True)
            #             df.reset_index(drop=True, inplace=True)
            #             #print(len(df))
            #         else:
            #             index += 1
            
            
            path = os.path.join(data_path,'audio',f)
            noise_path = os.path.join(data_path,'audio_noise')
            source_path = os.path.join(data_path,'audio_source')
            # if len(class_columns)>1:
            #     import pdb;pdb.set_trace()
            # print("Processing file {}, Length {}".format(f, audio.shape[1]/sr))
            ### saving audio
            start_noise = 0
            for index, row in df.iterrows():
                # print(" {}, {}, {}-{}".format(index,row["File Offset (s)"], row["Starttime"]+row["File Offset (s)"],row["Endtime"]+row["File Offset (s)"]))
                start = np.maximum(0,int(row["Starttime"]*sr) - int(FRONT*sr))
                end = int((row["Endtime"]-FRONT)*sr) + int(TAIL*sr)
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
                    if write_source:
                        torchaudio.save(os.path.join(source_path,os.path.basename(f).replace(".wav","_{}.wav".format(index))), audio_source, sr)
                    # audio_noise = (audio_noise - audio_noise.min())/(audio_noise.max() - audio_noise.min())*2 - 1
                    #write the noise occurring before the event
                    # print("Noise {} Duration: {} {} {}".format(index, end_noise/sr-start_noise/sr,start_noise/sr,end_noise/sr))
                    if write_noise and end_noise>start_noise and end_noise-start_noise>MIN_DURATION*sr:
                        if audio_noise.shape[-1]<MIN_DURATION_NOISE*sr:
                            audio_noise = torch.tile(audio_noise, (1,int(np.ceil(MIN_DURATION_NOISE*sr/audio_noise.shape[-1]))))[:,:int(MIN_DURATION_NOISE*sr)]
                        torchaudio.save(os.path.join(noise_path,os.path.basename(f).replace(".wav","_{}.wav".format(index))), audio_noise, sr)
                    start_noise = end
            #write the remaining noise
            # print("Duration: {}, {}-{}".format(audio.shape[1]/sr-start_noise/sr,start_noise/sr,audio.shape[1]/sr))
            if write_noise and start_noise<audio.shape[1] and audio.shape[1]-start_noise>MIN_DURATION*sr:
                audio_noise = audio[:,start_noise:]
                if audio_noise.shape[-1]<MIN_DURATION_NOISE*sr:
                    audio_noise = torch.tile(audio_noise, (1,int(np.ceil(MIN_DURATION_NOISE*sr/audio_noise.shape[-1]))))[:,:int(MIN_DURATION_NOISE*sr)]
                # audio_noise = (audio_noise - audio_noise.min())/(audio_noise.max() - audio_noise.min())*2 - 1
                torchaudio.save(os.path.join(noise_path,os.path.basename(f).replace(".wav","_{}.wav".format(index+1))), audio_noise, sr)
                
            

# Links to the audio files
REMOTES = {
    "dev": download.RemoteFileMetadata(
        filename="Development_Set.zip",
        url="https://zenodo.org/record/6482837/files/Development_Set.zip?download=1",
        checksum="cf4d3540c6c78ac2b3df2026c4f1f7ea",
    ),
    "train-classes": download.RemoteFileMetadata(
        filename="DCASE2022_task5_Training_set_classes.csv",
        url="https://zenodo.org/record/6482837/files/DCASE2022_task5_Training_set_classes.csv?download=1",
        checksum="abce1818ba10436971bad0b6a3464aa6",
    ),
    "validation-classes": download.RemoteFileMetadata(
        filename="DCASE2022_task5_Validation_set_classes.csv",
        url="https://zenodo.org/record/6482837/files/DCASE2022_task5_Validation_set_classes.csv?download=1",
        checksum="0c05ff0c9e1662ff8958c4c812abffdb",
    ),
    "eval": download.RemoteFileMetadata(
        filename="Evaluation_set_5shots.zip",
        url="https://zenodo.org/record/6517414/files/Evaluation_set_5shots.zip?download=1",
        checksum="5212c0e133874bba1ee25c81ced0de99",
        destination_dir="Evaluation_Set"
    ),
}



