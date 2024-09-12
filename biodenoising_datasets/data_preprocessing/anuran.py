import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
This is a public dataset for benchmarking Neotropical anuran calls classification.
For more information check the paper:
@article{akbal2023explainable,
  title={Explainable automated anuran sound classification using improved one-dimensional local binary pattern and Tunable Q Wavelet Transform techniques},
  author={Akbal, Erhan and Barua, Prabal Datta and Dogan, Sengul and Tuncer, Turker and Acharya, U Rajendra},
  journal={Expert Systems with Applications},
  volume={225},
  pages={120089},
  year={2023},
  publisher={Elsevier}
}
downloaded from: https://www.kaggle.com/datasets/mehmetbayin/anuran-sound-frogs-or-toads-dataset
'''
scientific_name_map = {1: 'Acris gryllus',
        2: 'Agalychnis callidryas', 
        3: 'Colostethus talamancae', 
        4: 'Alytes Cisternasii', 
        5: 'Alytes muletensis', 
        6: 'Ameerega cainarachi', 
        7: 'Anaxyrus cognatus', 
        8: 'Anaxyrus quercicus', 
        9: 'Centrolene savage', 
        10: 'Dendrobates leucomelas', 
        11: 'Dendrobates tinctorius azureus', 
        12: 'Eleutherodactylus pallidus', 
        13: 'Eleutherodactylus unistrigatus', 
        14: 'Gastrotheca riobambae', 
        15: 'Hyla squirella', 
        16: 'Hylarana laterimaculata', 
        17: 'Kaloula pulchra', 
        18: 'Microhyla butleri', 
        19: 'Microhyla heymonsi', 
        20: 'Microhyla ornate', 
        21: 'Oophaga granulifera', 
        22: 'Oophaga pumilio', 
        23: 'Rhinella Marina', 
        24: 'Scaphiopus couchii', 
        25: 'Smilisca baudinii', 
        26: 'Spea multiplicata'}   
common_name_map = {1: 'Southern cricket frog',  # Acris gryllus
        2: 'Red-eyed tree frog',  # Agalychnis callidryas
        3: 'Allobates talamancae',  # Colostethus talamancae
        4: 'Iberian midwife toad',  # Alytes Cisternasii
        5: 'Majorcan midwife toad',  # Alytes muletensis
        6: 'Cainarachi poison frog',  # Ameerega cainarachi
        7: 'Great Plains toad',  # Anaxyrus cognatus
        8: 'Oak toad',  # Anaxyrus quercicus
        9: 'Glass frog',  # Centrolene savage
        10: 'Yellow-banded poison dart frog',  # Dendrobates leucomelas
        11: 'Blue poison dart frog',  # Dendrobates tinctorius azureus
        12: 'Mexico endemic',  # Eleutherodactylus pallidus
        13: 'Pristimantis unistrigatus',  # Eleutherodactylus unistrigatus
        14: 'Andean marsupial tree frog',  # Gastrotheca riobambae
        15: 'Squirrel tree frog',  # Hyla squirella
        16: 'Side-spotted swamp frog',  # Hylarana laterimaculata
        17: 'Banded bullfrog',  # Kaloula pulchra
        18: 'Painted chorus frog',  # Microhyla butleri
        19: 'Dark-sided chorus frog',  # Microhyla heymonsi
        20: 'Ornate narrow-mouthed frog',  # Microhyla ornate
        21: 'Granular poison frog',  # Oophaga granulifera
        22: 'Strawberry poison-dart frog',  # Oophaga pumilio
        23: 'Cane toad',  # Rhinella Marina
        24: 'Couch\'s spadefoot toad',  # Scaphiopus couchii
        25: 'Common Mexican tree frog',  # Smilisca baudinii
        26: 'New Mexico spadefoot toad'}  # Spea multiplicata   

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='anuran', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        files = [f for f in os.listdir(os.path.join(self.path, 'Anuran_Sound')) if f.endswith('.flac')]
        for f in files:
            code = int(f.split('.flac')[0].split(' (')[0]) + 1
            caption = common_name_map[code]
            caption2 = scientific_name_map[code]
            url= 'https://www.kaggle.com/datasets/mehmetbayin/anuran-sound-frogs-or-toads-dataset'
            source = 'Anuran_Sound'
            recordist = ''
            species_common = common_name_map[code]
            species_scientific = scientific_name_map[code]
            audiocap_id = ''
            youtube_id = ''
            start_time = 0
            medium = 'terrestrial'
            species = scientific_name_map[code]
            relative_path = os.path.join('Anuran_Sound', f)
            row = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
            self.df.loc[len(self.df)] = row
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

        

# Links to the audio files
REMOTES = {
    "archive": download.RemoteFileMetadata(
        filename="Anuran_Sound.zip",
        url="gs://ml-bioacoustics-datasets/Anuran_Sound.zip",
        checksum="ded5ca5c7fad6d0dc2d1d2f2d341fcde",
    )
}
