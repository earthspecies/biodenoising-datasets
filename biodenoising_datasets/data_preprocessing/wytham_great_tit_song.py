'''
'''
import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public dataset containing great tit songs from the Wytham dataset.
@article{recalde2024densely,
  title={A densely sampled and richly annotated acoustic data set from a wild bird population},
  author={Recalde, Nilo Merino and Estand{\'\i}a, Andrea and Pichot, Loanne and Vansse, Antoine and Cole, Ella F and Sheldon, Ben C},
  journal={Animal Behaviour},
  volume={211},
  pages={111--122},
  year={2024},
  publisher={Elsevier}
}
The dataset is not directly accessible from the internet. You can manually download the dataset from the following link: https://osf.io/n8ac9/
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='anuraset', *args, **kwargs):
        self.path = path
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "song_files": 
        download.RemoteFileMetadata(
            filename="song-files.zip",
            url="gs://biodenoising-datasets/wytham_great_tit_song/song-files.zip",
            checksum="415990669a97e21fb9067821f2322e07",
        )
}



