import os
import pandas as pd
from . import download
from .AudioDataset import AudioDataset
'''
Watkins Marine Mammal Sound Database, Woods Hole Oceanographic Institution and the New Bedford Whaling Museum.
https://whoicf2.whoi.edu/science/B/whalesounds/about.cfm
'''
watkins_dict = {
    'Narwhal': 'Monodon monoceros',
    'Clymene_Dolphin': 'Stenella clymene',
    'Southern_Right_Whale': 'Eubalaena australis',
    'Harp_Seal': 'Pagophilus groenlandicus',
    'Grampus,_Rissos_Dolphin': 'Grampus griseus',
    'Beluga,_White_Whale': 'Delphinapterus leucas',
    'Pantropical_Spotted_Dolphin': 'Stenella attenuata',
    'Minke_Whale': 'Balaenoptera acutorostrata',
    'Bottlenose_Dolphin': 'Tursiops truncatus',
    'Bowhead_Whale': 'Balaena mysticetus',
    'Striped_Dolphin': 'Stenella coeruleoalba',
    'Frasers_Dolphin': 'Lagenodelphis hosei',
    'Weddell_Seal': 'Leptonychotes weddellii',
    'Atlantic_Spotted_Dolphin': 'Stenella frontalis',
    'Humpback_Whale': 'Megaptera novaeangliae',
    'Ross_Seal': 'Ommatophoca rossii',
    'Melon_Headed_Whale': 'Peponocephala electra',
    'Sperm_Whale': 'Physeter macrocephalus',
    'Bearded_Seal': 'Erignathus barbatus',
    'Short-Finned_Pacific_Pilot_Whale': 'Globicephala macrorhynchus',
    'Leopard_Seal': 'Hydrurga leptonyx',
    'False_Killer_Whale': 'Pseudorca crassidens',
    'Long-Finned_Pilot_Whale': 'Globicephala melas',
    'Fin,_Finback_Whale': 'Balaenoptera physalus',
    'Common_Dolphin': 'Delphinus delphis',
    'Killer_Whale': 'Orcinus orca',
    'White-beaked_Dolphin': 'Lagenorhynchus albirostris',
    'Rough-Toothed_Dolphin': 'Steno bredanensis',
    'Spinner_Dolphin': 'Stenella longirostris',
    'Walrus': 'Odobenus rosmarus',
    'White-sided_Dolphin': 'Lagenorhynchus acutus',
    'Northern_Right_Whale': 'Eubalaena glacialis'
}

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='watkins', *args, **kwargs):
        self.path = path
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        folders = [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]
        for d in folders:
            files = [f for f in os.listdir(os.path.join(self.path, d)) if f.endswith('.wav')]
            for f in files:
                caption2 = watkins_dict[d]
                caption = d.replace(',_', ' ').replace('_', ' ')
                url= 'https://whoicf2.whoi.edu/science/B/whalesounds/about.cfm'
                source = 'Watkins Marine Mammal Sound Database'
                recordist = ''
                species_scientific = watkins_dict[d]
                species_common = d.replace(',_', ' ').replace('_', ' ')
                audiocap_id = ''
                youtube_id = ''
                start_time = 0
                medium = 'underwater'
                species = watkins_dict[d]
                relative_path = os.path.join(d, f)
                row = {'dirs':'all','medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                self.df.loc[len(self.df)] = row
        self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "watkins": download.RemoteFileMetadata(
        filename="watkins.zip",
        url="https://archive.org/download/watkins_202104/watkins.zip",
        checksum="afef4877fb0b91c9952a68e436707179",
    )
}
