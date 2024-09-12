import os
from . import download
from .AudioDataset import AudioDataset, ALLOWED_EXTENSIONS
''' 
This is a public dataset from the orcasound project. This subset contains ocean noises.
For more information, please access the website: 
https://www.orcasound.net/
'''
DIRS = ['Train', 'Validation']

class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orcasound_sep_noise', *args, **kwargs):
        self.path = path
        self.all_dirs = {d:os.path.join(self.path,d) for d in DIRS if os.path.isdir(os.path.join(self.path,d))}
        assert len(self.all_dirs)>0 , "No directory found in {}".format(self.path)   
        self.splits = DIRS
        self.audio_files = {}
        for k,path in self.all_dirs.items():
            self.audio_files[k] = [os.path.join(root,file) for root,fdir,files in os.walk(path) for file in files if file.endswith(tuple(ALLOWED_EXTENSIONS)) and 'noise' in file and not file.startswith('.')]
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "all": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/acoustic-separation/dataset/",
            checksum="",
        ),
}
