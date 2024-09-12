import os
from . import download
from .AudioDataset import AudioDataset
''' 
This is a public domain dataset of instrumental sounds from the Good-Sounds corpus.
@inproceedings{bandiera2016good,
  title={Good-sounds. org: A framework to explore goodness in instrumental sounds},
  author={Bandiera, Giuseppe and Romani Picas, Oriol and Tokuda, Hiroshi and Hariya, Wataru and Oishi, Koji and Serra, Xavier},
  booktitle={Devaney J, Mandel MI, Turnbull D, Tzanetakis G, editors. ISMIR 2016. Proceedings of the 17th International Society for Music Information Retrieval Conference; 2016 Aug 7-11; New York City (NY).[Canada]: ISMIR; 2016. p. 414-9.},
  year={2016},
  organization={International Society for Music Information Retrieval (ISMIR)}
}
'''
class Dataset(AudioDataset):
    def __init__(self, conf, dname='goodsounds', write_tfrecord=True, recompute=False):
        super(Dataset, self).__init__(conf, dname)
        

# Links to the audio files
REMOTES = {
    "all": download.RemoteFileMetadata(
        filename="good-sounds.zip",
        url="https://zenodo.org/record/820937/files/good-sounds.zip?download=1",
        checksum="2137bbb2d32c1d60aa51e1301225f541",
    )
}



