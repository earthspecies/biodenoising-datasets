'''
DO NOT USE The NOCALLS class may occasionally have a few calls in it
'''
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orcasound project. This subset contains ocean noises.
For more information, please access the website: 
https://www.orcasound.net/
'''
class Dataset(AudioDataset):
    def __init__(self, conf, dname='orcasound_aldev_noise', *args, **kwargs):
        super(Dataset, self).__init__(conf, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "train": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/orcaal-dev/labeled/mp3/nocalls/",
            checksum="",
        ),
    "test": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/orcaal-dev/labeled_test/mp3/nocalls/",
            checksum="",
        ),
}
