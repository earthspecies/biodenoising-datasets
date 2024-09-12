from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset from the orcasound project. This subset contains ship noises.
For more information, please access the website: 
https://www.orcasound.net/
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='orcasound_shipnoise', *args, **kwargs):
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "shipsnet": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://shipnoise-net/realtime_files/",
            checksum="",
        ),
    "sandbox": 
        download.RemoteFileMetadata(
            filename="dir",
            url="s3://acoustic-sandbox/2017_8_VesselsAndWavS/",
            checksum="",
        )
}
