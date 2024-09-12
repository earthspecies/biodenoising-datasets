import os
from . import download
from .AudioDataset import AudioDataset


class Dataset(AudioDataset):
    def __init__(self, conf, path, dname='carrion_crows_denoising', *args, **kwargs):
        self.path = path
        ### replace path in the noise, clean and noisy json files
        for sr in [16000,48000]:
            folder_path = os.path.join(path,str(sr))  
            with open(os.path.join(folder_path,'noisy.json'), 'r') as f:
                noisy_list = json.load(f)
            for i in range(len(noisy_list)):
                noisy_list[i][0] = os.path.join(folder_path,'noisy',os.path.basename(noisy_list[i][0]))
            with open(os.path.join(folder_path,'noisy.json'), 'w') as f:
                json.dump(noisy_list, f)
            with open(os.path.join(folder_path,'clean.json'), 'r') as f:
                clean_list = json.load(f)
            for i in range(len(clean_list)):
                clean_list[i][0] = os.path.join(folder_path,'clean',os.path.basename(clean_list[i][0]))
            with open(os.path.join(folder_path,'clean.json'), 'w') as f:
                json.dump(clean_list, f)
            with open(os.path.join(folder_path,'noise.json'), 'r') as f:
                noise_list = json.load(f)
            for i in range(len(noise_list)):
                noise_list[i][0] = os.path.join(folder_path,'noise',os.path.basename(noise_list[i][0]))
            with open(os.path.join(folder_path,'noise.json'), 'w') as f:
                    json.dump(noise_list, f)
        super(Dataset, self).__init__(conf, path, dname, *args, **kwargs)
        

# Links to the audio files
REMOTES = {
    "dataset": download.RemoteFileMetadata(
        filename="dir",
        url="gs://biodenoising-datasets/carrion_crows_denoising",
        checksum="",
    ),
}
