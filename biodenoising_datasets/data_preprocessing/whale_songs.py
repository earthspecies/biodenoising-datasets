'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a private ESP dataset containing whale songs.
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='whale_songs', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    # "zip1": download.RemoteFileMetadata(
    #     filename="Hawaii\ Recordings.zip",
    #     url="gs://whale_song/Hawaii\ Recordings.zip",
    #     checksum="dsadadsa",
    # ),
    "zip2": download.RemoteFileMetadata(
        filename="Salish\ Sea\ Recordings.zip",
        url="gs://whale_song/Salish\ Sea\ Recordings.zip",
        checksum="dsadsadsad",
    ),
    # "zip3": download.RemoteFileMetadata(
    #     filename="Tahiti\ Whale\ Song.zip",
    #     url="gs://whale_song/Tahiti\ Whale\ Song.zip",
    #     checksum="dsadsa",
    # ),
    
}



