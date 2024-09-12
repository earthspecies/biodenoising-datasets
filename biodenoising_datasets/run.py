"""!
@brief Data processing script 
"""
import os
import argparse
import yaml
import tqdm
import torch
import asteroid
import random
import numpy as np

import data_preprocessing
import utils
ALLOWED_EXTENSIONS = set(['.wav','.mp3','.flac','.ogg','.aif','.aiff','.wmv'])

torch.use_deterministic_algorithms(True)

def seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)

def download(conf):
    g = torch.Generator()
    g.manual_seed(conf["output"]["seed"])

    os.makedirs(conf["main_args"]["input_path"], exist_ok=True)
    os.makedirs(conf["main_args"]["output_path"], exist_ok=True)
    
    for dname,dataset in conf["input"].items():
        dataset_path = os.path.join(conf["main_args"]["input_path"],dataset["path"])
        os.makedirs(os.path.join(conf["main_args"]["output_path"],dataset["split"],dataset["tag"],dname), exist_ok=True)
        os.makedirs(os.path.join(conf["main_args"]["output_path"],"metadata",dataset["split"],dataset["tag"]), exist_ok=True)
        #### Data downloading
        if dataset["download"] and hasattr(data_preprocessing, dname):
            download=True  
            if os.path.isdir(dataset_path):
                filelist = [os.path.join(root,file) for root,fdir,files in os.walk(dataset_path) for file in files if file.endswith(tuple(ALLOWED_EXTENSIONS)) and os.path.isfile(os.path.join(root, file))]
                if len(filelist)>0:
                    download=False
                    print("Found audio files in {}, skipping download. Delete them if you want to re-download.".format(dataset_path))
            if download:
                REMOTES = utils.my_import("data_preprocessing."+dname+".REMOTES")
                if "urbansound" in dname.lower() or "biodenoising_validation" in dname.lower():
                    download_path = conf["main_args"]["input_path"]
                else:
                    download_path = dataset_path
                data_preprocessing.download.downloader(
                    download_path,
                    remotes=REMOTES,
                    partial_download=None,
                    info_message="Downloading " + dname,
                    force_overwrite=False,
                    cleanup=False,
                )

            #### Data generation
            if not conf["main_args"]["download_only"]:
                print("Generating data for {}...".format(dname))
                dataset_class = utils.my_import("data_preprocessing."+dname+".Dataset")
                dataset = dataset_class(conf, dataset_path, dname, write_audio=True, write_tfrecord=False)
                if 'targetsr' in conf["output"] and len(conf["main_args"]["output_path"])>0:
                    for split in dataset.splits:
                        dataset.split = split
                        print("Split {}...".format(split))
                        for i in range(dataset.nparts):
                            print("Part {}...".format(i))
                            dataset.partid = i
                            dataset.init_parts_audio()
                            batch_size = 1
                            nworkers = 1 if dataset.nparts>1 else conf["main_args"]["nworkers"]
                            dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, pin_memory=False, num_workers=nworkers,generator=g, shuffle=False)
                            for j,batch_audio in enumerate(tqdm.tqdm(dataloader)):
                                pass
                    dataset.write_audio_length()
                



if __name__ == "__main__":

    # Keys which are not in the conf.yml file can be added here.
    # In the hierarchical dictionary created when parsing, the key `key` can be
    # found at dic['main_args'][key]

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", type=str, default='cfg/config16.yml', help="the config file for data generation"
    )
    parser.add_argument(
        "--input_path", type=str, required=True, help="the local path where to store the datasets"
    )
    parser.add_argument(
        "--output_path", type=str, default='', help="the local path where to generate the datasets"
    )
    parser.add_argument(
        "--nworkers", type=int, default=5, help="the number of workers for data generation"
    )
    parser.add_argument(
        "--download_only",action='store_true',help="Do not write any files, just download the data."
    )
    args = parser.parse_args()
    arg_dic = dict(vars(args))
    config = arg_dic["config"]
    with open(config) as f:
        def_conf = yaml.safe_load(f)
    parser = asteroid.utils.prepare_parser_from_dict(def_conf, parser=parser)
    arg_dic, plain_args = asteroid.utils.parse_args_as_dict(parser, return_plain_args=True)

    download(arg_dic)

#### python run.py --input_path /home/$USER/data/ --output_path /home/$USER/data/biodenoising16k --config cfg/config16.yml
#### python run.py --input_path /home/$USER/data/ --output_path /home/$USER/data/ --config cfg/validation.yml --download_only