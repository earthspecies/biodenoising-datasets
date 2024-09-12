import os
import torch
import torchaudio
import datetime
import random
import pandas as pd
from . import download
from .AudioDataset import AudioDataset, ALLOWED_EXTENSIONS
''' 
This is a public subset of underwater noises from the NOAA SanctSound project.
For more information, please check the website:https://sanctuaries.noaa.gov/news/feb21/sanctsound-overview.html
'''
SITES = ['ci01','ci02','ci03','ci04','ci05','fk01','fk02','fk03','fk04','gr01','gr02','gr03',
        'hi01','hi03','hi04','hi05','hi06','mb01','mb02','mb03','oc01','oc02','oc03','oc04',
        'pm01','pm02','pm05','sb01','sb02','sb03']
noise_classes = ['sonar','ships','explosions','unknown']
NELEMENTS = 10
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='noaa_sanctsound_noise', *args, **kwargs):
        self.path = path
        sites = [site for site in SITES if os.path.isdir(os.path.join(self.path,'audio',site))]
        self.all_dirs = {}
        assert len(sites)>0 , "No directory found in {}".format(self.path)   
        
        self.all_files = {}
        audio_dir = os.path.join(self.path,'audio')
        detection_dir = os.path.join(self.path,'products','detections')
        for site in sites:
            subsites = [f for f in os.listdir(os.path.join(audio_dir,site)) if os.path.isdir(os.path.join(audio_dir,site,f)) and not f.startswith('.')]
            for subsite in subsites:
                key = subsite.replace("sanctsound_","")
                all_files = []
                audio_list = [f for f in os.listdir(os.path.join(audio_dir,site,subsite,'audio')) if f.endswith(tuple(ALLOWED_EXTENSIONS)) and not f.startswith('.')]
                detected_classes = [f for f in os.listdir(os.path.join(detection_dir,site)) if os.path.isdir(os.path.join(detection_dir,site,f)) and f.lower().startswith(subsite) and not f.lower().endswith(tuple(noise_classes))]
                df = pd.DataFrame(columns=['ISOStartTime','ISOEndTime','class','start','end'])
                for c in detected_classes:
                    csv_files =  [f for f in os.listdir(os.path.join(detection_dir,site,c,'data')) if f.lower().endswith('.csv') and not f.startswith('.')]
                    df_file = pd.read_csv(os.path.join(detection_dir,site,c,'data',csv_files[0]))
                    df_file['class'] = c.split('_')[-1]
                    df_file['start'] = pd.to_datetime(df_file['ISOStartTime'])#, format='ISO8601')
                    if 'ISOEndTime' not in df_file.columns:
                        df_file['end'] = df_file['start'] + pd.Timedelta(hours=0, minutes=0, seconds=30)
                    else:
                        df_file['end'] = pd.to_datetime(df_file['ISOEndTime'])#, format='ISO8601')
                    df = pd.concat([df, df_file], ignore_index=True)
                for f in audio_list:
                    if not self.has_events(os.path.join(audio_dir,site,subsite,'audio',f), df):
                        all_files.append(os.path.join(audio_dir,site,subsite,'audio',f))
                
                #### create multiple smaller splits to avoid memory issues
                # if len(all_files)>0:
                #     for i in range(0,len(all_files), NELEMENTS):
                #         self.all_files[key+'_'+str(i)] = all_files[i:i+NELEMENTS]
                #         self.all_dirs[key+'_'+str(i)] = os.path.join(audio_dir,site,subsite,'audio')
                self.all_files[key] = all_files
                self.all_dirs[key] = os.path.join(audio_dir,site,subsite,'audio')
        import pdb;pdb.set_trace()          
        self.splits = list(self.all_dirs.keys())
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)


    def has_events(self, path, df_all):
        f = os.path.basename(path)
        #import pdb;pdb.set_trace()
        timestamp = [t for t in f.split('.')[0].split('_') if len(t)==16 or len(t)==12][0]
        if len(timestamp)==12:
            timestamp = '20' + timestamp[:6] + 'T' + timestamp[6:]
        start=pd.Timestamp(timestamp).tz_localize(None)
        
        ### loading audio
        metadata = torchaudio.info(path)
        duration = metadata.num_frames / metadata.sample_rate 
        end = start + pd.Timedelta(hours=0, minutes=0, seconds=duration)
        if 'Presence' in df_all.columns:
            df = df_all[(df_all['start']>start) & (df_all['start']<end) & (df_all['Presence']==1)]
        else:
            df = df_all[(df_all['start']>start) & (df_all['start']<end)] 
        if len(df)>0:
            return True
        else:
            return False
        
# Links to the audio files
REMOTES = {
    "ci01_01_audio": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/ci01/sanctsound_ci01_01/audio/",
            checksum="",
            destination_dir="audio/ci01/sanctsound_ci01_01/",
        ),
    "ci01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/ci01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "gr01_01_audio": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/gr01/sanctsound_gr01_01/audio/",
            checksum="",
            destination_dir="audio/gr01/sanctsound_gr01_01/",
        ),
    "gr01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/gr01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "fk02_01_audio": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk02/sanctsound_fk02_01/audio/",
            checksum="",
            destination_dir="audio/fk02/sanctsound_fk02_01/",
        ),
    "fk02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/fk02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "oc02_01_audio": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/oc02/sanctsound_oc02_01/audio/",
            checksum="",
            destination_dir="audio/oc02/sanctsound_oc02_01/",
        ),
    "oc02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/oc02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "mb02_01_audio": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/mb02/sanctsound_mb02_01/audio/",
            checksum="",
            destination_dir="audio/mb02/sanctsound_mb02_01/",
        ),
    "mb02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/mb02/",
            checksum="",
            destination_dir="products/detections/",
        )
}
