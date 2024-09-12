# biodenoising-datasets
biodenoising-datasets is a lightweight Python library to download and process datasets that are used in denoising of animal vocalizations. 

By working with the config files and run.py script, you can download and validate the datasets, extract the vocalizations and the noise excerpts

The datasets and the library were used in the following paper:

```Marius Miron, Sara Keen, Jen-Yu Liu, Benjamin Hoffman, Masato Hagiwara, Olivier Pietquin, Felix Effenberger, Maddie Cusimano, "Biodenoising: animal vocalization denoising without access to clean data"```

Here we provide the code to download the data. The training code is at the [github repo](https://github.com/earthspecies/biodenoising). If you solely plan to do inference go to the following [github repo](https://github.com/earthspecies/biodenoising-inference)

Check the [biodenoising web page](https://mariusmiron.com/research/biodenoising) for demos and more info.

## Installation
Create an environment with your favorite package manager (Python<=3.11) and install the dependencies:

```
git clone https://github.com/biodenoising/biodenoising-datasets.git
cd biodenoising-datasets
pip install -r requirements.txt
```

## Usage

### Downloading the datasets

The script run.py downloads the datasets and extracts the vocalizations and the noise excerpts. For instance, to download the datasets in the cfg/config16.yml. 

```
python run.py --input_path /home/$USER/data/ --output_path /home/$USER/data/biodenoising16k --config cfg/config16.yml
python run.py --input_path /home/$USER/data/ --output_path /home/$USER/data/ --config cfg/validation.yml --download_only
```

where --input_path is the local path where to store the datasets and --output_path is the local path where to generate the datasets.

### Writing your own config file

You can write your own config file to download and process your list of datasets. The config file is a yaml file and you can find an example in cfg/config16.yml.

First you need to define the output data config, the maximum length of the audio files, the target sample rate, and the seed for the random number generator.

```
output:
  audio_timelength: 30.0 
  targetsr: 16000
  seed: 42
```

Then you need to define the list of datasets:

```
  macaques:
    download: yes
    path: macaques
    time_stretch: no
    add_offset: no
    repeat: no
    sample_rate: 44100
    tag: clean
    split: train
  geladas:
    download: yes
    path: geladas
    time_stretch: no
    add_offset: no
    repeat: no
    sample_rate: 44100
    tag: noisy
    split: dev
```

The fields tag and split are used to define the folders where the audio files are stored with the path: /home/$USER/data/biodenoising16k/tag/split/dataset_name/. 

### TO DO list

- [ ] Write metadata for the datasets - currently implemented only for anuran
- [ ] Audioset loader with metadata
- [ ] Xeno-Canto full dataset with metadata
- [ ] Refactor tfrecord generation