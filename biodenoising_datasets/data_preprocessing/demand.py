'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a subset of DEMAND, a public dataset for benchmarking environmental sound classification.
For more information check the paper:
@inproceedings{thiemann2013diverse,
  title={The diverse environments multi-channel acoustic noise database (demand): A database of multichannel environmental noise recordings},
  author={Thiemann, Joachim and Ito, Nobutaka and Vincent, Emmanuel},
  booktitle={Proceedings of Meetings on Acoustics},
  volume={19},
  number={1},
  year={2013},
  organization={AIP Publishing}
}
'''
DIRS = {'NFIELD':"sports field", 'NPARK':"city park"}
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='demand', *args, **kwargs):
        self.path = path
        self.all_dirs = {d:os.path.join(self.path,d) for d in DIRS if os.path.isdir(os.path.join(self.path,d))}
        assert len(self.all_dirs)>0 , "No directory found in {}".format(self.path)   
        self.splits = list(DIRS.keys())
        self.df =  pd.DataFrame(columns=['dirs','medium','caption','caption2','url','source','recordist','species_common','species_scientific','audiocap_id','youtube_id','start_time','species','relative_path'])
        for d,v in DIRS.items():
            files = [f for f in os.listdir(os.path.join(self.path, d)) if f.endswith('.wav')]
            for f in files:
                caption = v
                caption2 =  ''
                url= 'https://zenodo.org/record/7551553'
                source = 'demand'
                recordist = ''
                species_common = ''
                species_scientific = ''
                audiocap_id = ''
                youtube_id = ''
                start_time = 0
                medium = 'terrestrial'
                species = ''
                relative_path = os.path.join(d, f)
                rowdf = {'dirs':d,'medium':medium,'caption':caption, 'caption2':caption2, 'url':url, 'source':source, 'recordist':recordist, 'species_common':species_common, 'species_scientific':species_scientific, 'audiocap_id':audiocap_id, 'youtube_id':youtube_id, 'start_time':start_time, 'species':species, 'relative_path':relative_path}
                self.df.loc[len(self.df)] = rowdf
            self.df.to_csv(os.path.join(self.path, 'metadata.csv'), index=False)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "field": download.RemoteFileMetadata(
        filename="NFIELD_48k.zip",
        url="https://zenodo.org/record/1227121/files/NFIELD_48k.zip?download=1",
        checksum="937eab7d3f64cea99fa377238e84c185",
    ),
    "park": download.RemoteFileMetadata(
        filename="NPARK.zip",
        url="https://zenodo.org/record/1227121/files/NPARK_48k.zip?download=1",
        checksum="bb90ec754ac02eede51bf80675a78cfe",
    ),
}



