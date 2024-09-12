from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orcasound project. This subset contains vocalizations.
For more information, please access the website: 
https://www.orcasound.net/
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orcasound_aldev', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "train": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/orcaal-dev/labeled/mp3/calls/",
            checksum="",
        ),
    "test": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/orcaal-dev/labeled_test/mp3/calls/",
            checksum="",
        ),
}
