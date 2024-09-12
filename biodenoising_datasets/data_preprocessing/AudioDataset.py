import os
import numpy as np
import torch
import torchaudio
import torch_time_stretch
import librosa
import pandas as pd
import soundfile as sf
import math
import tfrecord
import functools
from scipy import stats
import pickle
import noisereduce as nr

ALLOWED_EXTENSIONS = set(['.wav','.mp3','.flac','.ogg','.aif','.aiff','.wmv','.WAV','.MP3','.FLAC','.OGG','.AIF','.AIFF','.WMV'])

torch.use_deterministic_algorithms(True)

g = torch.Generator()
g.manual_seed(42)

class AudioDataset(torch.utils.data.IterableDataset):
# class AudioDataset(torch.utils.data.Dataset):
    def __init__(self, conf, path, dname, write_tfrecord=False, write_audio=True):
        '''
        input:  conf (dict), dname (str)
        '''
        if not hasattr(self, "path"):
            self.path = path
        config_code = conf["main_args"]["config"].split(os.path.sep)[-1].split('.')[0]

        self.dataset_name = dname
        self.conf = conf
        self.n_samples = 0
        
            
        if "split" in conf["input"][dname]:
            self.split_out = conf["input"][dname]["split"]
        else:
            self.split_out = ''

        if "shard_size" in conf["input"][dname]:
            self.shard_size = conf["input"][dname]["shard_size"]
        else:
            self.shard_size = 1000
        self.tag = conf["input"][dname]["tag"]

        self.audio_timelength = conf["output"]["audio_timelength"]

        if "targetsr" in conf["output"]:
            self.targetsr = conf["output"]["targetsr"]
            self.time_samples = int(self.audio_timelength*self.targetsr)
        else:
            self.targetsr = None
            self.time_samples = int(self.audio_timelength*conf["input"][dname]["sample_rate"])
            
        if "noresample" in conf["output"]:
            self.noresample = conf["output"]["noresample"]
        else:
            self.noresample = False
            
        self.time_stretch = conf["input"][dname]["time_stretch"]

        self.add_offset = conf["input"][dname]["add_offset"]
        self.repeat = conf["input"][dname]["repeat"]
        self.write_tfrecord = write_tfrecord
        self.write_audio = write_audio
        
        if "nparts" in conf["input"][dname]:
            self.nparts = int(conf["input"][dname]["nparts"])
        else:
            self.nparts = 1
        self.partid = 0
        self.offset_parts = 0
        
        self.writers = {}
        self.tfrecords_path = {}
        self.nworkers = {}
        if hasattr(self, "df"):
            assert len(self.df) > 0, "Dataframe is empty"
            self.splits = self.df["dirs"].unique()
            self.df = self.df.sort_values("dirs")
            self.df = self.df.reset_index(drop=True)
            self.audio_files = {}
            for split in self.splits:
                df_split = self.df[self.df["dirs"] == split]
                self.audio_files[split] = [os.path.join(self.path, rel_path) for rel_path in df_split['relative_path'].values]
        elif hasattr(self, "all_dirs"):
            if not hasattr(self, "audio_files"):
                self.audio_files = {}
            for k,path in self.all_dirs.items():
                if k not in self.audio_files.keys():
                    self.audio_files[k] = [os.path.join(root,file) for root,fdir,files in os.walk(path) for file in files if file.endswith(tuple(ALLOWED_EXTENSIONS)) and not file.startswith('.')]
        else:
            self.all_dirs = {'all': self.path}
            if not hasattr(self, "audio_files"):
                self.audio_files = {'all':[os.path.join(root,file) for root,fdir,files in os.walk(self.path) for file in files if file.endswith(tuple(ALLOWED_EXTENSIONS)) and not file.startswith('.')]}
        
        #### tfrecords are create for dataset, split, part 
        self.split = 'all'
        if not hasattr(self, "splits"):
            self.splits = ['all']
        else:
            self.split = self.splits[0]
            
        #### get indices and offsets for all files
        self.indices = {}
        self.offsets = {}
        self.n_samples = {}
        self.nsamples_per_file = {}
        for k in self.splits:
            chunks_nsamples = [self.get_nchunks(audio) for audio in self.audio_files[k]]
            chunks_per_file = [item[0] for item in chunks_nsamples]
            nsamples_per_file = [item[1] for item in chunks_nsamples]
            self.nsamples_per_file[k] = {f: n  for f, n in zip(self.audio_files[k], nsamples_per_file)}
            num_points = np.cumsum(np.array([0]+[chunks_per_file[i] for i in range(len(chunks_per_file))], dtype=int))
            self.indices[k], self.offsets[k] = self.get_indices(chunks_per_file)
            self.n_samples[k] = num_points[-1]
        
        self.nworkers[self.split] = int(math.ceil(self.n_samples[self.split]/self.shard_size))
        
        if hasattr(self, "df"):
            self.create_dataframe()

    def split_chunks(self, audio):
        '''
        input: audio (torch.tensor), sr (int), chunk_size (int)
        output: chunks (list of torch.tensor)
        '''
        # Split audio into chunks 
        chunks = torch.split(audio, self.time_samples)
        return torch.stack(chunks)
    
    def get_nchunks(self, path):
        '''
        input: path (str)
        output: nchunks (int)
        '''
        ### loading audio metadata
        try:
            metadata = torchaudio.info(path)
            duration = metadata.num_frames / metadata.sample_rate 
            sample_rate = metadata.sample_rate
        except Exception as e:
            duration = librosa.get_duration(filename=path)
            sample_rate = librosa.get_samplerate(path)
            # audio, sample_rate = sf.read(path)
            # duration = len(audio)/sample_rate

        if self.targetsr is not None and sample_rate!=self.targetsr :
            if sample_rate<self.targetsr and ('noise' in self.tag or self.noresample):
                total_samples = int(duration * sample_rate)
            else:
                total_samples = int(duration * self.targetsr)
        else:
            total_samples = int(duration * sample_rate)
        nchunks = int(math.ceil(total_samples/self.time_samples))
        return nchunks, total_samples

    def get_indices(self, chunks_per_file):
        '''
        input: num_points (list)
        output: indices (list), offsets (list)  
        '''
        indices = []
        offsets = []
        for i,c in enumerate(chunks_per_file):
            indices.extend([i for j in range(c)])
            offsets.extend([j for j in range(c)])
        return indices, offsets
            
    def wavread(self, path):
        '''
        input: path (str)
        output: audio (torch.tensor)
        '''
        ### loading audio
        try:
            audio, sr = torchaudio.load(path, normalize=True)
            audio = audio.float()
        except Exception as e:
            # audio, sr = sf.read(path)
            audio, sr = librosa.load(path, sr=None)
            audio = librosa.util.normalize(audio)
            audio = torch.from_numpy(audio).float()

        ### stereo to mono 
        if len(audio.shape)==2:
            if audio.shape[0] > audio.shape[1]:
                audio = audio.transpose(0,1)
            audio = audio.sum(dim=0) 
        time_samples = len(audio)   
        # print(sr)
        ### resampling
        if self.targetsr is not None and sr!=self.targetsr :
            ### for the noise samples of lower sample rate we don't do any stretching and resampling 
            ### we just play the noisy audio faster
            if sr<self.targetsr and 'noise' not in self.tag and not self.noresample:
                if (sr/self.targetsr)<0.8 and self.time_stretch:
                    ratios = torch_time_stretch.get_fast_stretches(sr)
                    ### compute the closest time stretch ratio
                    ratio = min(ratios, key=lambda x:abs(x.numerator/x.denominator-sr/self.targetsr))
                    audio = torch_time_stretch.time_stretch(audio[None,None,:], ratio, sr)[0,0,:]
                    # print("Time stretching {} from {} to {}".format(path, sr, self.targetsr))

                ### resample    
                true_ratio = self.targetsr/sr
                ### this torchaudio resampling is very slow
                # audio = torchaudio.transforms.Resample(sr, self.targetsr, rolloff=0.8, lowpass_filter_width=10)(audio)
                audio=torch.from_numpy(librosa.resample(y=audio.to('cpu').numpy(), orig_sr=sr, target_sr=self.targetsr)).float()
                # print("Resampling {} from {} to {}".format(path, sr, self.targetsr))
                
                ### ensure the number of time samples
                expected_time_samples = int(true_ratio * time_samples)
                if len(audio)>expected_time_samples:
                    audio = audio[:expected_time_samples]
                elif len(audio)<expected_time_samples:
                    audio = torch.cat((audio,torch.zeros(expected_time_samples-len(audio))))
            elif sr>self.targetsr:
                # audio = torchaudio.transforms.Resample(sr, self.targetsr)(audio)
                audio=torch.from_numpy(librosa.resample(y=audio.to('cpu').numpy(), orig_sr=sr, target_sr=self.targetsr)).float()
            
            sr = self.targetsr 
            
        return audio,sr
    
    @functools.lru_cache()
    def load_audio(self, audio_file):
        '''
        input: audio_file (str)
        output: audio (torch.tensor)
        '''

        ### loading audio
        audio,sr = self.wavread(audio_file)
        
        if self.add_offset: ### usually for sources 
            ### right zero padding to add initial time delay
            pad_length = len(audio)%self.time_samples
            if pad_length>0:
                nframes_pad = int(np.random.uniform() * pad_length)
                audio = torch.cat((torch.zeros(nframes_pad),audio))

            ### left zero padding 
            if len(audio)%self.time_samples!=0:
                audio = torch.cat((audio, torch.zeros(self.time_samples-len(audio)%self.time_samples)))
        else:
            ### repeat the signal to make it a multiple of time_samples
            if len(audio)%self.time_samples!=0:
                if len(audio)>self.time_samples:
                    audio = torch.cat((audio, audio[:self.time_samples-len(audio)%self.time_samples]))
                elif self.repeat:
                    audio = audio.repeat(math.ceil(self.time_samples/len(audio)))
                    audio =  audio[:self.time_samples]

        if len(audio)> self.time_samples:
            audio = self.split_chunks(audio)
        else:
            audio = audio.view(1,-1)
        return audio, sr
    
    def gen_poisson(self,mu):
        """Adapted from https://github.com/rmalouf/learning/blob/master/zt.py"""
        r = np.random.uniform(low=stats.poisson.pmf(0, mu))
        return int(stats.poisson.ppf(r, mu))
    
    def __len__(self):
        total_samples = int(math.ceil(self.n_samples[self.split] / self.nparts))
        return total_samples
    
    def init_writers(self):
        total_shards = int(math.ceil(self.n_samples[self.split]/self.shard_size))
        part_total_shards = int(math.ceil(total_shards/self.nparts))
        range_parts = range(self.partid*part_total_shards, (self.partid+1)*part_total_shards)
        if self.targetsr is not None:
            self.tfrecords_path[self.split] = [os.path.join(self.conf["output"]["path"],self.conf["input"][self.dataset_name]["tag"] + '_'+ self.dataset_name+'_'+self.split+'_'+str(self.targetsr)+'_'+str(i)+".tfrecord") for i in range_parts]
        else:
            self.tfrecords_path[self.split] = [os.path.join(self.conf["output"]["path"],self.conf["input"][self.dataset_name]["tag"] + '_'+ self.dataset_name+'_'+self.split+'_'+str(i)+".tfrecord") for i in range_parts]
        self.writers[self.split] = [tfrecord.TFRecordWriter(self.tfrecords_path[self.split][i]) for i in range(len(self.tfrecords_path[self.split]))]
        self.nworkers[self.split] = len(self.tfrecords_path[self.split])
        self.offset_parts = self.partid * self.shard_size
        print("number of tfrecords {} for {}, {}, {}".format(len(self.tfrecords_path[self.split]), self.dataset_name, self.split, self.partid))
        
    def init_parts_audio(self):
        total_samples = int(math.ceil(self.n_samples[self.split] / self.nparts))
        self.offset_parts = self.partid * total_samples

    def close_writers(self):    
        for w in self.writers[self.split]:
            w.close()
        for path in self.tfrecords_path[self.split]:
            tfrecord.tools.tfrecord2idx.create_index(path,path.replace('.tfrecord','.index'))
            
    def create_dataframe(self):
        df = pd.DataFrame(columns=self.df.columns) 
        i = 0
        for split in self.splits:
            df_split = self.df[self.df["dirs"] == split]
            total_samples = int(math.ceil(self.n_samples[split] / self.nparts))
            for idx in range(total_samples):
                splitext = os.path.splitext(self.audio_files[split][self.indices[split][idx]])
                filename =  self.dataset_name + '_' + split + '_'+ str(idx) + '_' + os.path.basename(splitext[0]) + '.wav'
                path = os.path.join(self.split_out,self.tag, self.dataset_name, filename)
                row = self.df.loc[self.indices[split][idx]]
                row['relative_path'] = path
                df.loc[i] = row
                i += 1
        df.drop(columns=['dirs'], inplace=True)
        metadata_path = os.path.join(self.conf["main_args"]["output_path"],"metadata",self.split_out,self.tag, self.dataset_name+'.csv')
        df.to_csv(metadata_path, index=False)
        
    def write_audio_length(self):
        metadata_path = os.path.join(self.conf["main_args"]["output_path"],"metadata",self.split_out,self.tag, self.dataset_name+'.csv')
        df = pd.read_csv(metadata_path)
        for i in range(len(df)):
            metadata = torchaudio.info(os.path.join(self.conf["main_args"]["output_path"],df.loc[i, 'relative_path']))
            duration = metadata.num_frames / metadata.sample_rate 
            sample_rate = metadata.sample_rate
            df.loc[i, "num_frames"] = metadata.num_frames
            df.loc[i, "sample_rate"] = metadata.sample_rate
        df.to_csv(metadata_path, index=False)
        
    def __iter__(self):
        total_samples = int(math.ceil(self.n_samples[self.split] / self.nparts))
        worker_info = torch.utils.data.get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            iter_start = self.offset_parts
            iter_end = np.minimum(self.offset_parts + total_samples, self.n_samples[self.split])
        else:  # in a worker process
            # split workload
            per_worker = int(math.ceil(total_samples / float(worker_info.num_workers)))
            worker_id = worker_info.id
            iter_start = self.offset_parts + worker_id * per_worker
            iter_end = np.minimum(iter_start + per_worker, self.n_samples[self.split])
        ### iterate over the audio files
        # print("iterating over {} from {} to {}".format(self.split, iter_start, iter_end))
        for idx in range(iter_start, iter_end):
            audio, sr = self.load_audio(self.audio_files[self.split][self.indices[self.split][idx]])
            if self.write_audio:
                splitext = os.path.splitext(self.audio_files[self.split][self.indices[self.split][idx]])
                filename =  self.dataset_name + '_' + self.split + '_'+ str(idx) + '_' + os.path.basename(splitext[0]) + '.wav'
                path = os.path.join(self.conf["main_args"]["output_path"],self.split_out,self.tag, self.dataset_name, filename)
                # print(path)
                
                if len(audio.shape)<3:
                    try:
                        audiow = audio[self.offsets[self.split][idx]].unsqueeze(dim=0)
                    except Exception as e:
                        return
                    
                elif len(audio.shape)==4:
                    audiow = audio[0,self.offsets[self.split][idx]]
                else:
                    audiow = audio[self.offsets[self.split][idx]]
                torchaudio.save(path, audiow, sr, format="wav")
            if self.write_tfrecord:
                writer_id = worker_id
                self.writers[self.split][writer_id].write({
                        "audio": (audio[self.offsets[self.split][idx]].numpy().astype(np.float32), "float"),
                        "sr": (sr, "int")
                    })
                if idx == iter_end-1:
                    self.writers[self.split][writer_id].close()
                    path = self.tfrecords_path[self.split][writer_id]
                    tfrecord.tools.tfrecord2idx.create_index(path,path.replace('.tfrecord','.index'))
            yield audio[self.offsets[self.split][idx]] 
            
    def slice_noise(self, audio_noise, sr, index, noise_path, f, min_duration=0.5, min_duration_noise=4., noise_reduce=True):
        ext = os.path.splitext(f)[-1]
        if noise_reduce:
            start_stop = self.activity_detector.detect_activity(nr.reduce_noise(audio_noise.numpy().squeeze(),sr), sr)
        else:
            start_stop = self.activity_detector.detect_activity(audio_noise.numpy().squeeze(), sr)
        if len(start_stop)>0:
            if start_stop[0,1]>start_stop[0,0] and start_stop[0,0]>min_duration:
                chunk_noise = audio_noise[:,:int(start_stop[0,0]*sr)]
                if chunk_noise.shape[-1]<min_duration_noise*sr:
                    chunk_noise = torch.tile(chunk_noise, (1,int(np.ceil(min_duration_noise*sr/chunk_noise.shape[-1]))))[:,:int(min_duration_noise*sr)]
                torchaudio.save(os.path.join(noise_path,f.replace(ext,"_{}_{}.wav".format(index, 0))), chunk_noise, sr)
            if len(start_stop)>2:
                for i in range(1,len(start_stop)):
                    if start_stop[i,1]>start_stop[i,0] and start_stop[i,0]-start_stop[i-1,1]>min_duration:
                        chunk_noise = audio_noise[:,int(start_stop[i-1,1]*sr):int(start_stop[i,0]*sr)]
                        if chunk_noise.shape[-1]<min_duration_noise*sr:
                            chunk_noise = torch.tile(chunk_noise, (1,int(np.ceil(min_duration_noise*sr/chunk_noise.shape[-1]))))[:,:int(min_duration_noise*sr)]
                        torchaudio.save(os.path.join(noise_path,f.replace(ext,"_{}_{}.wav".format(index, i))), chunk_noise, sr)
            if len(start_stop)>1 and start_stop[-1,1]>start_stop[-1,0] and audio_noise.shape[1]/sr-start_stop[-1,1]>min_duration:
                chunk_noise = audio_noise[:,int(start_stop[-1,1]*sr):]
                if chunk_noise.shape[-1]<min_duration_noise*sr:
                    chunk_noise = torch.tile(chunk_noise, (1,int(np.ceil(min_duration_noise*sr/chunk_noise.shape[-1]))))[:,:int(min_duration_noise*sr)]
                torchaudio.save(os.path.join(noise_path,f.replace(ext,"_{}_{}.wav".format(index, len(start_stop)+1))), chunk_noise, sr)
        else:
            torchaudio.save(os.path.join(noise_path,f.replace(ext,"_{}.wav".format(index))), audio_noise, sr)