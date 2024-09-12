'''
may contain calls, not just noise, annotations were provided by authors separately 
'''
import os
from . import download
from .AudioDataset import AudioDataset
'''
This is a public dataset containing underwater fjord sounds. It may containing underwater mammal sounds.
For more information, check the following zenodo record: https://zenodo.org/records/3402649
'''
class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='underwater_fjords', *args, **kwargs):
        self.path = path
        assert os.path.exists(self.path) , "No directory found in {}".format(self.path)   
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)

# Links to the audio files
REMOTES = {
    "audio1": download.RemoteFileMetadata(
        filename="5146.190719125517.wav",
        url="https://zenodo.org/record/3402649/files/5146.190719125517.wav?download=1",
        checksum="a332815290a5f79a3abfd74c2a559caa",
    ),
    "audio2": download.RemoteFileMetadata(
        filename="5146.190719131953.wav",
        url="https://zenodo.org/record/3402649/files/5146.190719131953.wav?download=1",
        checksum="e3b15c2554053621e20782b5fe586bb0",
    ),
    "audio3": download.RemoteFileMetadata(
        filename="5146.190719141953.wav",
        url="https://zenodo.org/record/3402649/files/5146.190719141953.wav?download=1",
        checksum="78218d70b5880a65f3a28c2729aa495c",
    ),
    "audio4": download.RemoteFileMetadata(
        filename="5146.190719161941.wav",
        url="https://zenodo.org/record/3402649/files/5146.190719161941.wav?download=1",
        checksum="71e53d705f36634ec14741f6dbb3d1eb",
    ),
    "audio5": download.RemoteFileMetadata(
        filename="5146.190719190657.wav",
        url="https://zenodo.org/record/3402649/files/5146.190719190657.wav?download=1",
        checksum="979dc793dcf6229b5f4ac00eff33767d",
    ),
    "audio6": download.RemoteFileMetadata(
        filename="5146.190720004447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720004447.wav?download=1",
        checksum="440c9f5e301afc62f1f241d3856be645",
    ),
    "audio7": download.RemoteFileMetadata(
        filename="5146.190720014447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720014447.wav?download=1",
        checksum="1a6f7442408c2c1cabcfac986f18e9e5",
    ),
    "audio8": download.RemoteFileMetadata(
        filename="5146.190720024447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720024447.wav?download=1",
        checksum="5d6a8e6acc66355406139c5883e22694",
    ),
    "audio9": download.RemoteFileMetadata(
        filename="5146.190720034447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720034447.wav?download=1",
        checksum="481fddd1f7cdbd0da22425f4a46c9b81",
    ),
    "audio10": download.RemoteFileMetadata(
        filename="5146.190720044447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720044447.wav?download=1",
        checksum="8875256a616c17fb8c7cc9b12d959681",
    ),
    "audio11": download.RemoteFileMetadata(
        filename="5146.190720054447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720054447.wav?download=1",
        checksum="eae5d405a70644582091acfee15b8828",
    ),
    "audio12": download.RemoteFileMetadata(
        filename="5146.190720064447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720064447.wav?download=1",
        checksum="6cda568859651476f772df708f2a4660",
    ),
    "audio13": download.RemoteFileMetadata(
        filename="5146.190720074447.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720074447.wav?download=1",
        checksum="797bd108377c4bc5be9289611da85a4b",
    ),
    "audio14": download.RemoteFileMetadata(
        filename="5146.190720130259.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720130259.wav?download=1",
        checksum="d7c50836b2a7ea0798b225c16e822fec",
    ),
    "audio15": download.RemoteFileMetadata(
        filename="5146.190720143026.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720143026.wav?download=1",
        checksum="5354be43f04f5569821d529ae388915d",
    ),
    "audio16": download.RemoteFileMetadata(
        filename="5146.190720151013.wav",
        url="https://zenodo.org/record/3402649/files/5146.190720151013.wav?download=1",
        checksum="b9c6057b55456bef7167a27e62d6472e",
    ),
    "audio17": download.RemoteFileMetadata(
        filename="sony.190719130533.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190719130533.WAV?download=1",
        checksum="29162139918610319bee0b261c19087e",
    ),
    "audio18": download.RemoteFileMetadata(
        filename="sony.190719132214.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190719132214.WAV?download=1",
        checksum="8e815d6f88d361067f6458f333f67bee",
    ),
    "audio19": download.RemoteFileMetadata(
        filename="sony.190719161154.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190719161154.WAV?download=1",
        checksum="b4b4ed999eccbf172c60250379e56640",
    ),
    "audio20": download.RemoteFileMetadata(
        filename="sony.190719190911.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190719190911.WAV?download=1",
        checksum="656ca749125784c75e2cf5cd56cef38e",
    ),
    "audio21": download.RemoteFileMetadata(
        filename="sony.190719130533.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190719130533.WAV?download=1",
        checksum="29162139918610319bee0b261c19087e",
    ),
    "audio22": download.RemoteFileMetadata(
        filename="sony.190720130442.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190720130442.WAV?download=1",
        checksum="a68fb69a4c50da0dc468f4eeb9e19378",
    ),
    "audio23": download.RemoteFileMetadata(
        filename="sony.190720140142.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190720140142.WAV?download=1",
        checksum="41db78c3f05a11ab1f9a3de61e7bc441",
    ),
    "audio24": download.RemoteFileMetadata(
        filename="sony.190720151110.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190720151110.WAV?download=1",
        checksum="641340cc4b8aae97f7524572435b8544",
    ),
    "audio25": download.RemoteFileMetadata(
        filename="sony.190721221704.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190721221704.WAV?download=1",
        checksum="1b9e4ceda77d22d1f8f9017b1dd47e6f",
    ),
    "audio26": download.RemoteFileMetadata(
        filename="sony.190721221953.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190721221953.WAV?download=1",
        checksum="27eeec4e5e9cf59c6b57ced0f00e200a",
    ),
    "audio27": download.RemoteFileMetadata(
        filename="sony.190722001234.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190722001234.WAV?download=1",
        checksum="cc337a39e634bc15c646e7df0444477a",
    ),
    "audio28": download.RemoteFileMetadata(
        filename="sony.190727132858.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727132858.WAV?download=1",
        checksum="edf3b40f8745503f2c4fe80789413784",
    ),
    "audio29": download.RemoteFileMetadata(
        filename="sony.190727141359.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727141359.WAV?download=1",
        checksum="89e59e316cfc637176c48a097a0d8f1e",
    ),
    "audio30": download.RemoteFileMetadata(
        filename="sony.190727155633.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727155633.WAV?download=1",
        checksum="d6cd9435db3159d42e92eefa5c2bb35a",
    ),
    "audio31": download.RemoteFileMetadata(
        filename="sony.190727170304.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727170304.WAV?download=1",
        checksum="d0659b49a72564b064d029fbba0b93d4",
    ),
    "audio32": download.RemoteFileMetadata(
        filename="sony.190727172216.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727172216.WAV?download=1",
        checksum="89b017f25891db3d34c6583113bd7143",
    ),
    "audio33": download.RemoteFileMetadata(
        filename="sony.190727175939.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727175939.WAV?download=1",
        checksum="0f605eecee79d7b52b268ab618a8586c",
    ),
    "audio34": download.RemoteFileMetadata(
        filename="sony.190727194432.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727194432.WAV?download=1",
        checksum="21ac57fef1a9af5c7b24985e5632eb8f",
    ),
    "audio35": download.RemoteFileMetadata(
        filename="sony.190727230712.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727230712.WAV?download=1",
        checksum="27bcbef21aed8d925574b7e1b15e6dd2",
    ),
    "audio36": download.RemoteFileMetadata(
        filename="sony.190727215707.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190727215707.WAV?download=1",
        checksum="34ed89b3b72dc29f324fdeda09bb9174",
    ),
    "audio37": download.RemoteFileMetadata(
        filename="sony.190728000241.WAV",
        url="https://zenodo.org/record/3402649/files/sony.190728000241.WAV?download=1",
        checksum="0b82522413900244b784b59fd95b2e9b",
    ),
}



