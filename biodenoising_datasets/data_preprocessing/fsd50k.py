import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
This is a subset of the FSD50K dataset, a public dataset of human-labeled sound events.
For more info check the paper:
@article{fonseca2021fsd50k,
  title={Fsd50k: an open dataset of human-labeled sound events},
  author={Fonseca, Eduardo and Favory, Xavier and Pons, Jordi and Font, Frederic and Serra, Xavier},
  journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing},
  volume={30},
  pages={829--852},
  year={2021},
  publisher={IEEE}
}

'''
# Global parameter
DIRS = ['FSD50K.eval_audio','FSD50K.dev_audio'] #,'FSD50K.dev_audio']
MIN_FILE_SIZE = 10000

NOISE_TAGS = ['Vehicle', 'Tearing', 'Liquid', 'Engine', 'Thunderstorm', 'Water', 'Crushing', 'Fire', 
    'Mechanisms', 'Tools', 'Motor_vehicle_(road)','Wind', 'Wood','Car', 'Rail_transport',
    'Aircraft', 'Rain', 'Power_tool', 'Ocean']
ALL_TAGS = ['Animal', 'Domestic_sounds_and_home_sounds', 'Music', 'Vehicle', 'Tearing', 'Human_voice',
    'Liquid', 'Explosion', 'Bell', 'Engine', 'Tap', 'Thump_and_thud', 'Burping_and_eructation',
    'Crumpling_and_crinkling', 'Walk_and_footsteps', 'Thunderstorm', 'Water', 'Fart', 'Squeak',
    'Respiratory_sounds', 'Human_group_actions', 'Crushing', 'Fire', 'Alarm', 'Glass', 'Chewing_and_mastication',
    'Whoosh_and_swoosh_and_swish', 'Mechanisms', 'Hands', 'Tools', 'Crack', 'Motor_vehicle_(road)',
    'Livestock_and_farm_animals_and_working_animals', 'Wind', 'Bird_vocalization_and_bird_call_and_bird_song',
    'Rattle', 'Speech', 'Hiss', 'Singing', 'Keyboard_(musical)', 'Screech', 'Wood', 'Shout', 'Run', 'Drum',
    'Crackle', 'Tick', 'Percussion', 'Plucked_string_instrument', 'Domestic_animals_and_pets', 'Insect',
    'Wild_animals', 'Cymbal', 'Pour', 'Laughter', 'Guitar', 'Door', 'Car', 'Bird', 'Rail_transport',
    'Aircraft', 'Rain', 'Power_tool', 'Ocean', 'Cough', 'Bowed_string_instrument', 'Clock', 'Drum_kit',
    'Mallet_percussion', 'Breathing', 'Cat', 'Typing', 'Brass_instrument', 'Telephone']

OTHER_TAGS = set(ALL_TAGS).symmetric_difference(set(NOISE_TAGS))



class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='fsd50k', *args, **kwargs):
        self.path = path
        self.audio_files = {}
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        self.process(conf,dname)
        
        self.all_dirs = {d:os.path.join(self.path,d) for d in DIRS if os.path.isdir(os.path.join(self.path,d))}
        assert len(self.all_dirs)>0 , "No directory found in {}".format(self.path)   
        self.splits = DIRS
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        
    def process(self, conf, dname):
        for d in DIRS:
            self.audio_files[d] = []
            csv = 'dev.csv' if d=='FSD50K.dev_audio' else 'eval.csv'
            metadata = os.path.join(self.path,'FSD50K.ground_truth', csv)
            df = pd.read_table(metadata, sep=',')
            for i in range(len(df.fname)):
                if not(set(df.labels[i].split(',')) & OTHER_TAGS):
                    if os.path.exists(os.path.join(self.path,d,str(df.fname[i])+'.wav')):
                        self.audio_files[d].append(os.path.join(self.path,d,str(df.fname[i])+'.wav'))
                        caption = df.labels[i]
                        caption2 = df.labels[i]
                        url= 'https://freesound.org'
                        source = 'fsd50k'
                        recordist = ''
                        species_common = ''
                        species_scientific = ''
                        audiocap_id = ''
                        youtube_id = ''
                        start_time = 0
                        medium = 'underwater' if 'Liquid' in df.labels[i] or 'Water' in df.labels[i] or 'Ocean' in df.labels[i] else 'terrestrial'
                        species = ''
                        relative_path = os.path.join(d,str(df.fname[i])+'.wav')
                        row = {'dirs':d,'medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                        self.df.loc[len(self.df)] = row
                
                
        

# Links to the audio files
REMOTES = {
    "FSD50K.dev_audio": [
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.zip",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.zip?download=1",
            checksum="c480d119b8f7a7e32fdb58f3ea4d6c5a",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.z01",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z01?download=1",
            checksum="faa7cf4cc076fc34a44a479a5ed862a3",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.z02",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z02?download=1",
            checksum="8f9b66153e68571164fb1315d00bc7bc",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.z03",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z03?download=1",
            checksum="1196ef47d267a993d30fa98af54b7159",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.z04",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z04?download=1",
            checksum="d088ac4e11ba53daf9f7574c11cccac9",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.dev_audio.z05",
            url="https://zenodo.org/record/4060432/files/FSD50K.dev_audio.z05?download=1",
            checksum="81356521aa159accd3c35de22da28c7f",
        ),
    ],
    "FSD50K.eval_audio": [
        download.RemoteFileMetadata(
            filename="FSD50K.eval_audio.zip",
            url="https://zenodo.org/record/4060432/files/FSD50K.eval_audio.zip?download=1",
            checksum="6fa47636c3a3ad5c7dfeba99f2637982",
        ),
        download.RemoteFileMetadata(
            filename="FSD50K.eval_audio.z01",
            url="https://zenodo.org/record/4060432/files/FSD50K.eval_audio.z01?download=1",
            checksum="3090670eaeecc013ca1ff84fe4442aeb",
        ),
    ],
    "ground_truth": download.RemoteFileMetadata(
        filename="FSD50K.ground_truth.zip",
        url="https://zenodo.org/record/4060432/files/FSD50K.ground_truth.zip?download=1",
        checksum="ca27382c195e37d2269c4c866dd73485",
    ),
    "metadata": download.RemoteFileMetadata(
        filename="FSD50K.metadata.zip",
        url="https://zenodo.org/record/4060432/files/FSD50K.metadata.zip?download=1",
        checksum="b9ea0c829a411c1d42adb9da539ed237",
    )
}


