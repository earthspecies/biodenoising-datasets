import os
from . import orcasound_bestos_noise
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orcasound project. This subset contains vocalizations.
For more information, please access the website: 
https://www.orcasound.net/
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orcasound_bestos', *args, **kwargs):
        self.path = path
        process = orcasound_bestos_noise.Dataset.__dict__["process"]
        self.process_file = orcasound_bestos_noise.Dataset.__dict__["process_file"]
        process(self,conf, dname)
        self.all_dirs = {'all':os.path.join(self.path,'audio_source')}
        self.splits = ['all']
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        
# Links to the audio files
REMOTES = {
    "all": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/2021_9_12_OS_YearsBestVocalPassby/hallo-annotation-test-SRKW/",
            checksum="",
        )
}
