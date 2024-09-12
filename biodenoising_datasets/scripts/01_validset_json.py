import argparse
import numpy as np
import os
import torchaudio
from collections import namedtuple

Info = namedtuple("Info", ["length", "sample_rate", "channels"])

parser = argparse.ArgumentParser(
        'prepare_experiments',
        description="Generate json files with all the audios")
parser.add_argument("--data_dir", type=str, required=True,
                    help="directory where the  data is")

def get_info(path):
    info = torchaudio.info(path)
    if hasattr(info, 'num_frames'):
        # new version of torchaudio
        return Info(info.num_frames, info.sample_rate, info.num_channels)
    else:
        siginfo = info[0]
        return Info(siginfo.length // siginfo.channels, siginfo.rate, siginfo.channels)
    
def to_csv(files, filename, args):
    meta = []
    for f in files:
        info = get_info(f)
        meta.append((os.path.basename(f), np.round(info.length/info.sample_rate,3), info.sample_rate))
    meta.sort()    
    fname = os.path.join(args.data_dir, filename)
    np.savetxt(fname, np.array(meta), delimiter=",", fmt='%s', header='filename,duration,sample_rate')
    
def generate_csv(args):
    clean_files = [os.path.join(args.data_dir,'clean',f) for f in os.listdir(os.path.join(args.data_dir,'clean'))]
    noise_files = [os.path.join(args.data_dir,'noise',f) for f in os.listdir(os.path.join(args.data_dir,'noise'))]
    
    to_csv(clean_files, 'clean.csv', args)
    to_csv(noise_files, 'noise.csv', args)

if __name__ == "__main__":
    args = parser.parse_args()
    generate_csv(args)
