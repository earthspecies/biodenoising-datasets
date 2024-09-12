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
SPLITS = ['ci','fk','gr','hi','mb','oc','pm','sb']
noise_classes = ['sonar','ships','explosions','unknown']
NELEMENTS = 10
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='noaa_sanctsound_small_noise', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        sites = [site for site in SITES if os.path.isdir(os.path.join(self.path,'audio',site))]
        self.all_dirs = {}
        assert len(sites)>0 , "No directory found in {}".format(self.path)   
        
        self.all_files = {}
        audio_dir = os.path.join(self.path,'audio')
        detection_dir = os.path.join(self.path,'products','detections')
        for site in sites:
            if not os.path.exists(os.path.join(audio_dir,site)):
                continue
            subsites = [f for f in os.listdir(os.path.join(audio_dir,site)) if os.path.isdir(os.path.join(audio_dir,site,f)) and not f.startswith('.')]
            split = site[:2]
            if split not in self.all_files.keys():
                self.all_files[split] = []
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
                        df_file['end'] = df_file['start'] + pd.Timedelta(hours=0, minutes=59, seconds=59)
                    else:
                        df_file['end'] = pd.to_datetime(df_file['ISOEndTime'])#, format='ISO8601')
                    df = pd.concat([df, df_file], ignore_index=True)
                df['start'] = df['start'].apply(lambda t: t.replace(tzinfo=None))
                df['end'] = df['end'].apply(lambda t: t.replace(tzinfo=None))
                for f in audio_list:
                    if not self.has_events(os.path.join(audio_dir,site,subsite,'audio',f), df):
                        all_files.append(os.path.join(audio_dir,site,subsite,'audio',f))
                    else:
                        continue
                    caption = "underwater noise"
                    caption2 =  ''
                    url= 'gs://noaa-passive-bioacoustic/sanctsound'
                    source = 'NOAA Sanctsound'
                    recordist = ''
                    species_common = '' 
                    species_scientific = ''
                    audiocap_id = ''
                    youtube_id = ''
                    start_time = 0
                    medium = 'underwater'
                    species = ''
                    relative_path = os.path.join('audio',site,subsite,'audio',f)
                    row = {'dirs':split,'medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                    self.df.loc[len(self.df)] = row
                self.all_files[split].extend(all_files)
                self.all_dirs[split] = os.path.join(audio_dir,site,subsite,'audio')      
        self.splits = list(self.all_dirs.keys())
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
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
    "fk01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/fk01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "oc01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/oc01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "mb01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/mb01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "fk01_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_FK01_01_671359016_20190419T172921Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk01/sanctsound_fk01_01/audio/SanctSound_FK01_01_671359016_20190419T172921Z.flac",
            checksum="",
            destination_dir="audio/fk01/sanctsound_fk01_01/audio/",
        ),
    "fk01_01_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_FK01_01_671359016_20190214T093147Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk01/sanctsound_fk01_01/audio/SanctSound_FK01_01_671359016_20190214T093147Z.flac",
            checksum="",
            destination_dir="audio/fk01/sanctsound_fk01_01/audio/",
        ),
    "oc01_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_OC01_01_671399974_20190717T174035Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/oc01/sanctsound_oc01_01/audio/SanctSound_OC01_01_671399974_20190717T174035Z.flac",
            checksum="",
            destination_dir="audio/oc01/sanctsound_oc01_01/audio/",
        ),
    "oc01_01_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_OC01_01_671399974_20190509T175044Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/oc01/sanctsound_oc01_01/audio/SanctSound_OC01_01_671399974_20190509T175044Z.flac",
            checksum="",
            destination_dir="audio/oc01/sanctsound_oc01_01/audio/",
        ),
    "mb01_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_MB01_01_671387685_20190328T110250Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/mb01/sanctsound_mb01_01/audio/SanctSound_MB01_01_671387685_20190328T110250Z.flac",
            checksum="",
            destination_dir="audio/mb01/sanctsound_mb01_01/audio/",
        ),
    "ci02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/ci02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "ci02_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_CI02_01_671117349_20190113T115553Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/ci02/sanctsound_ci02_01/audio/SanctSound_CI02_01_671117349_20190113T115553Z.flac",
            checksum="",
            destination_dir="audio/ci02/sanctsound_ci02_01/audio/",
        ),
    "gr02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/gr02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "gr02_02_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_GR02_02_470331456_190923071500.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/gr02/sanctsound_gr02_02/audio/SanctSound_GR02_02_470331456_190923071500.flac",
            checksum="",
            destination_dir="audio/gr02/sanctsound_gr02_02/audio/",
        ),
    "gr02_02_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_GR02_02_470331456_190809151457.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/gr02/sanctsound_gr02_02/audio/SanctSound_GR02_02_470331456_190809151457.flac",
            checksum="",
            destination_dir="audio/gr02/sanctsound_gr02_02/audio/",
        ),
    "ci01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/ci01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "gr01_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/gr01/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "fk02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/fk02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "oc02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/oc02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "mb02_detection": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/sanctsound/products/detections/mb02/",
            checksum="",
            destination_dir="products/detections/",
        ),
    "ci01_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_CI01_01_671379494_20181125T145604Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/ci01/sanctsound_ci01_01/audio/SanctSound_CI01_01_671379494_20181125T145604Z.flac",
            checksum="",
            destination_dir="audio/ci01/sanctsound_ci01_01/audio/",
        ),
    "ci01_01_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_CI01_01_671379494_20181117T175718Z",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/ci01/sanctsound_ci01_01/audio/SanctSound_CI01_01_671379494_20181117T175718Z.flac",
            checksum="",
            destination_dir="audio/ci01/sanctsound_ci01_01/audio/",
        ),
    "ci01_01_audio03": 
        download.RemoteFileMetadata(
            filename="SanctSound_CI01_01_671379494_20181213T072652Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/ci01/sanctsound_ci01_01/audio/SanctSound_CI01_01_671379494_20181213T072652Z.flac",
            checksum="",
            destination_dir="audio/ci01/sanctsound_ci01_01/audio/",
        ),
    "gr01_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_GR01_01_671363112_20190425T151533Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/gr01/sanctsound_gr01_01/audio/SanctSound_GR01_01_671363112_20190425T151533Z.flac",
            checksum="",
            destination_dir="audio/gr01/sanctsound_gr01_01/audio/",
        ),
    "gr01_01_audio03": 
        download.RemoteFileMetadata(
            filename="SanctSound_GR01_01_671363112_20190414T110951Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/gr01/sanctsound_gr01_01/audio/SanctSound_GR01_01_671363112_20190414T110951Z.flac",
            checksum="",
            destination_dir="audio/gr01/sanctsound_gr01_01/audio/",
        ),
    "fk02_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_FK02_01_671117353_20190213T152203Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk02/sanctsound_fk02_01/audio/SanctSound_FK02_01_671117353_20190213T152203Z.flac",
            checksum="",
            destination_dir="audio/fk02/sanctsound_fk02_01/audio/",
        ),
    "fk02_01_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_FK02_01_671117353_20190102T212800Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk02/sanctsound_fk02_01/audio/SanctSound_FK02_01_671117353_20190102T212800Z.flac",
            checksum="",
            destination_dir="audio/fk02/sanctsound_fk02_01/audio/",
        ),
    "fk02_01_audio03": 
        download.RemoteFileMetadata(
            filename="SanctSound_FK02_01_671117353_20190413T014011Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/fk02/sanctsound_fk02_01/audio/SanctSound_FK02_01_671117353_20190413T014011Z.flac",
            checksum="",
            destination_dir="audio/fk02/sanctsound_fk02_01/audio/",
        ),
    "oc02_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_OC02_01_671621160_20190405T235536Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/oc02/sanctsound_oc02_01/audio/SanctSound_OC02_01_671621160_20190405T235536Z.flac",
            checksum="",
            destination_dir="audio/oc02/sanctsound_oc02_01/audio/",
        ),
    "oc02_01_audio03": 
        download.RemoteFileMetadata(
            filename="SanctSound_OC02_01_671621160_20190319T055801Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/oc02/sanctsound_oc02_01/audio/SanctSound_OC02_01_671621160_20190319T055801Z.flac",
            checksum="",
            destination_dir="audio/oc02/sanctsound_oc02_01/audio/",
        ),
    "mb02_01_audio01": 
        download.RemoteFileMetadata(
            filename="SanctSound_MB02_01_671903780_20190213T225614Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/mb02/sanctsound_mb02_01/audio/SanctSound_MB02_01_671903780_20190213T225614Z.flac",
            checksum="",
            destination_dir="audio/mb02/sanctsound_mb02_01/audio/",
        ),
    "mb02_01_audio02": 
        download.RemoteFileMetadata(
            filename="SanctSound_MB02_01_671903780_20181127T135758Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/mb02/sanctsound_mb02_01/audio/SanctSound_MB02_01_671903780_20181127T135758Z.flac",
            checksum="",
            destination_dir="audio/mb02/sanctsound_mb02_01/audio/",
        ),
    "mb02_01_audio03": 
        download.RemoteFileMetadata(
            filename="SanctSound_MB02_01_671903780_20181231T195029Z.flac",
            url="gs://noaa-passive-bioacoustic/sanctsound/audio/mb02/sanctsound_mb02_01/audio/SanctSound_MB02_01_671903780_20181231T195029Z.flac",
            checksum="",
            destination_dir="audio/mb02/sanctsound_mb02_01/audio/",
        ),
}
