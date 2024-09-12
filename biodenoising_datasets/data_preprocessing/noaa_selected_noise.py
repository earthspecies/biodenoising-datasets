import os
from . import download
from .AudioDataset import AudioDataset, ALLOWED_EXTENSIONS
''' 
This is a public subset of underwater noises from the NOAA SanctSound project.
For more information, please check the website:https://sanctuaries.noaa.gov/news/feb21/sanctsound-overview.html
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='noaa_selected_noise', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)


# Links to the audio files
REMOTES = {
    "coastal_studies_institute": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/coastal_studies_institute/audio/ncroep/hat01/",
            checksum="",
            destination_dir="coastal_studies_institute",
        ),
    "swfsc": 
        download.RemoteFileMetadata(
            filename="dir",
            url="gs://noaa-passive-bioacoustic/swfsc/audio/",
            checksum="",
            destination_dir="swfsc",
        ),
}
