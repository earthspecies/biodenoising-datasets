import os
import io 
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
''' 
This is a private dataset containing underwater vessel noises.
For more information, please access the following paper:
@article{santos2016shipsear,
  title={ShipsEar: An underwater vessel noise database},
  author={Santos-Dom{\'\i}nguez, David and Torres-Guijarro, Soledad and Cardenal-L{\'o}pez, Antonio and Pena-Gimenez, Antonio},
  journal={Applied Acoustics},
  volume={113},
  pages={64--69},
  year={2016},
  publisher={Elsevier}
}
The dataset can be obtained by contacting the authors.
'''
CSV = """ID,Name,Type
    80,Adricristuy,Dredger
    10,Mar de Onza (Leaving),Passengers
    14,Pirata de Cies (Waiting),Passengers
    15,Rada Uno (Passing),Tugboat
    6,Mar de Cangas (Entering),Passengers
    7,Mar de Cangas (Waiting),Passengers
    13,Pirata de Cies (Entering),Passengers
    11,Minho Uno (Entering),Passengers
    12,Minho Uno (Leaving),Passengers
    17,Mar de Mouro (Entering),Passengers
    8,Mar de Onza (Entering),Passengers
    9,Mar de Onza (Waiting),Passengers
    16,MSC Opera,Ocean liner
    21,Motorboat,Motorboat
    18,Autopride (Entering),RORO
    19,Autopride(reverse),RORO
    20,Autopride(preparing maneuver),RORO
    38,Arroios,Passengers
    40,Mar de Cangas (arrives interference),Passengers
    43,Pirata de Cies (arrives interference),Passengers
    42,Pirata de Cies (leaves),Passengers
    41,Minho uno (arrives),Passengers
    39,Motorboat Duda (arrives),Motorboat
    45,Yacht (leaves),Motorboat
    26,Motorboat,Motorboat
    27,Motorboat (close recording),Motorboat
    28,Nuevo ria Aldan,Trawler
    31,Tugboat (start-stop engine),Tugboat
    29,Pilot ship,Pilot ship
    30,Pilot ship,Pilot ship
    24,Adventure of the seas (slowing),Ocean liner
    25,Adventure of the seas (arrives),Ocean liner
    22,Adventure of the seas (maneuver),Ocean liner
    23,Adventure of the seas (stopped),Ocean liner
    37,Sailboat (starts and leaves),Sailboat
    36,Minho uno (leaving),Passengers
    34,Mar de Onza (arrives),Passengers
    33,Duda (going out),Motorboat
    35,Mar de Onza (going out),Passengers
    32,Arroios (arrives),Passengers
    46,Mussel boat1,Mussel boat
    54,Pirata de Salvora (leaves),Passengers
    56,Sailboat,Sailboat
    57,Sailboat 2,Sailboat
    47,Mussel boat2,Mussel boat
    50,Motorboat1,Motorboat
    48,Mussel boat3 (interf),Mussel boat
    53,Pirata de Salvora (arrives),Passengers
    51,Motorboat2 (interf),Motorboat
    52,Motorboat3 (interf),Motorboat
    49,ussel boat4,Mussel boat
    55,Pirata de Salvora (leaves 2nd take),Passengers
    62,Mar de Cangas (leaves),Passengers
    63,Mar de Onza (arrives),Passengers
    67,Pirata de Cies,Passengers
    58,Eimskip Reefer (interf),RORO
    66,Fishboat,Mussel boat
    60,Mar de Cangas (arrives),Passengers
    59,Mar de Mouro (arrives),Passengers
    65,Minho uno (arrives),Passengers
    61,Mar de Cangas (leaves 2),Passengers
    64,Mar de Onza (leaves),Passengers
    68,Sailboat,Sailboat
    71,Discovery UK,Ocean liner
    77,High speed motorboat,Motorboat
    75,Fishboat 1,Fishboat
    79,Zodiac,Motorboat
    73,Mari Carmen fishboat,Fishboat
    76,Fishboat 2,Fishboat
    72,Motorboat 2,Motorboat
    74,Saladino Primero,fishboat
    70,Small yacht,Motorboat
    69,Costa Voyager,Ocean liner
    78,Viking Chance,RORO
    85,Natural ambient noise sample 1,Natural ambient noise
    86,Natural ambient noise sample 2,Natural ambient noise
    87,Natural ambient noise sample 3,Natural ambient noise
    88,Natural ambient noise sample 4,Natural ambient noise
    89,Natural ambient noise sample 5,Natural ambient noise
    90,Natural ambient noise sample 6,Natural ambient noise
    91,Natural ambient noise sample 7,Natural ambient noise
    92,Natural ambient noise sample 8,Natural ambient noise
    81,Maximum Flow,Natural ambient noise
    83,Maximum wave,Natural ambient noise
    82,Maximum rain,Natural ambient noise
    84,Maximum wind,Natural ambient noise
    93,Moanha tests sample 1,Dredger
    94,Moanha tests sample 2,Dredger
    95,Moanha tests sample 3,Dredger
    96,Moanha tests sample 4,Dredger"""

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='shipsear', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path) 
        metadata = pd.read_csv(io.StringIO(CSV), sep=",")  
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        files = [f for f in os.listdir(os.path.join(self.path, 'shipsEar_AUDIOS')) if f.endswith('.wav')]
        for f in files:
            idx = int(f.split('__')[0])
            row = metadata.loc[metadata['ID']==idx]
            caption = row['Type'].values[0] if row['Type'].values[0] != 'Natural ambient noise' else row['Name'].values[0]
            caption2 = ''
            url= ''
            source = 'ShipsEar'
            recordist = ''
            species_common = '' 
            species_scientific = ''
            audiocap_id = ''
            youtube_id = ''
            start_time = 0
            medium = 'underwater'
            species = ''
            relative_path = os.path.join('shipsEar_AUDIOS', f)
            rowdf = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
            self.df.loc[len(self.df)] = rowdf
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "full": 
        download.RemoteFileMetadata(
            filename="shipsEar_AUDIOS-20230722T064202Z-001.zip",
            url="gs://shipsear/shipsEar_AUDIOS-20230722T064202Z-001.zip",
            checksum="6c31a05b784848e1a28776fa0ea8ddc1",
        ),
}
