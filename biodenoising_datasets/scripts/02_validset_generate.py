import argparse
import numpy as np
import os
import json
import torch
import torchaudio
import math
import pandas as pd
import librosa
import scipy
import random

parser = argparse.ArgumentParser(
        'generate biodenoising validation set',
        description="Generate json files with all the audios")
parser.add_argument("--data_dir", type=str, required=True,
                    help="directory where the data is")

SAMPLE_RATES = [16000,48000]
MIN_DURATION = 4. # (seconds)
SAMPLE_DURATION = 4. # (seconds)
LOW_SNR = -5
HIGH_SNR = 10
SEED = 42 # make sure we get the same dataset when this is ran twice

### set the random seed
torch.manual_seed(SEED)
random.seed(SEED)
np.random.seed(SEED)
torch.backends.cudnn.deterministic = True
torch.use_deterministic_algorithms(True) 
rng = random.Random(SEED)
rngnp = np.random.default_rng(seed=SEED)

def generate_mix(row, row_noise, index, sr, snr, args, generate_snrs=True, suffix=''):
        audio_clean, _ = wavread(os.path.join(args.data_dir,'clean',row['filename']),'clean',sr)   
        audio_noise, _ = wavread(os.path.join(args.data_dir,'noise',row_noise['filename']),'noise',sr)
        if audio_clean.shape[1]<SAMPLE_DURATION*sr:
            #random zero pad clean
            audio_clean = torch.cat((audio_clean,torch.zeros(1,int(SAMPLE_DURATION*sr)-audio_clean.shape[1])), dim=1)
            audio_final = torch.zeros((audio_clean.shape[0],int(SAMPLE_DURATION*sr)), device=audio_clean.device)
            pad_left = rng.randint(0,int(SAMPLE_DURATION*sr)-audio_clean.shape[1])
            audio_final[...,pad_left:pad_left+audio_clean.shape[-1]] = audio_clean
            audio_clean = audio_final
        if audio_noise.shape[1]<audio_clean.shape[1]:
            #repeat noise
            audio_noise = audio_noise.repeat((1,int(math.ceil(audio_clean.shape[1]/audio_noise.shape[1]))))
            audio_noise =  audio_noise[:,:audio_clean.shape[1]]
        elif audio_noise.shape[1]>audio_clean.shape[1]:
            nframes_offset = int(rngnp.uniform() * (audio_noise.shape[1]-audio_clean.shape[1]))
            audio_noise =  audio_noise[:,nframes_offset:nframes_offset+audio_clean.shape[1]]    

        audio_noisy = torchaudio.functional.add_noise(waveform=audio_clean, noise=audio_noise, snr=snr)
        if abs(audio_noisy).max()>1:
            audio_noisy = audio_noisy/abs(audio_noisy).max()
            audio_clean = audio_clean/abs(audio_noisy).max()
            audio_noise = audio_noise/abs(audio_noisy).max()
        
        if suffix == '_sample':
            ### build sample dataset
            if audio_clean.shape[1]//sr > SAMPLE_DURATION:
                peaks = get_peaks(audio_clean[0,:].numpy(), sr)
                idx = np.argmax(audio_clean[0,peaks*sr].numpy())
                start = np.maximum(0,int(sr*(peaks[idx] - SAMPLE_DURATION/2)))
                diff = abs(int(sr*(peaks[idx] - SAMPLE_DURATION/2))) - start
                end = diff+int(sr*(peaks[idx] + SAMPLE_DURATION/2))
                sample_noisy = audio_noisy[:,start:end]
                sample_clean = audio_clean[:,start:end]
                sample_noise = audio_noise[:,start:end]
            else:
                sample_noisy = audio_noisy 
                sample_clean = audio_clean
                sample_noise = audio_noise
                audio_clean = audio_clean[:,:int(MIN_DURATION*sr)]
                audio_noisy = audio_noisy[:,:int(MIN_DURATION*sr)]
                audio_noise = audio_noise[:,:int(MIN_DURATION*sr)]
        
        # ### save
        torchaudio.save(os.path.join(args.data_dir,str(sr)+suffix,'clean',str(index)+'_'+row['type']+'.wav'), audio_clean, sr)
        torchaudio.save(os.path.join(args.data_dir,str(sr)+suffix,'noisy',str(index)+'_'+row['type']+'.wav'), audio_noisy, sr)
        torchaudio.save(os.path.join(args.data_dir,str(sr)+suffix,'noise',str(index)+'_'+row['type']+'.wav'), audio_noise, sr)
        
        meta_json_clean=(os.path.join(args.data_dir,str(sr)+suffix,'clean',str(index)+'_'+row['type']+'.wav'), audio_clean.shape[1])
        meta_json_noisy=(os.path.join(args.data_dir,str(sr)+suffix,'noisy',str(index)+'_'+row['type']+'.wav'), audio_noisy.shape[1])
        meta_csv=(str(index)+'_'+row['type']+'.wav', audio_clean.shape[1], sr, snr.numpy()[0], row['filename'],row_noise['filename'],row['type'])
        
        meta_json_clean_snr = {snr:[] for snr in [-5, 0, 5, 10]}
        meta_json_noisy_snr = {snr:[] for snr in [-5, 0, 5, 10]}
        meta_csv_snr = {snr:[] for snr in [-5, 0, 5, 10]}
        if generate_snrs:
            for snr in [-5, 0, 5, 10]:
                audio_noisy = torchaudio.functional.add_noise(waveform=audio_clean, noise=audio_noise, snr=torch.tensor([snr]), lengths=None)
                if abs(audio_noisy).max()>1:
                    audio_noisy = audio_noisy/abs(audio_noisy).max()
                    audio_clean = audio_clean/abs(audio_noisy).max()
                    audio_noise = audio_noise/abs(audio_noisy).max()
                torchaudio.save(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'clean',str(index)+'_'+row['type']+'.wav'), audio_clean, sr)
                torchaudio.save(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noisy',str(index)+'_'+row['type']+'.wav'), audio_noisy, sr)
                torchaudio.save(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noise',str(index)+'_'+row['type']+'.wav'), audio_noise, sr)

                meta_json_clean_snr[snr].append((os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'clean',str(index)+'_'+row['type']+'.wav'), audio_clean.shape[1]))
                meta_json_noisy_snr[snr].append((os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noisy',str(index)+'_'+row['type']+'.wav'), audio_noisy.shape[1]))
                meta_csv_snr[snr].append((str(index)+'_'+row['type']+'.wav', audio_clean.shape[1], sr, snr, row['filename'],row_noise['filename'],row['type']))
            
        return meta_csv, meta_json_clean, meta_json_noisy, meta_csv_snr, meta_json_clean_snr, meta_json_noisy_snr
        
def pair_files(df_clean,df_noise,sr,args):
    df_clean.sort_values(by=['duration'],ascending=False,inplace=True)
    df_noise.sort_values(by=['duration'],ascending=False,inplace=True)
    snrs = [torch.tensor([rngnp.uniform(LOW_SNR, HIGH_SNR)]) for _ in range(len(df_clean))]
    snrs_large = [torch.tensor([rngnp.uniform(LOW_SNR, HIGH_SNR)]) for _ in range(len(df_clean)*len(df_noise))]
    transform = torch.nn.Sequential(torchaudio.transforms.AddNoise())
    #iterate through dataframes
    meta_json_clean = []
    meta_json_noisy = []
    meta_csv = []
    meta_json_clean_snr = {snr:[] for snr in [-5, 0, 5, 10]}
    meta_json_noisy_snr = {snr:[] for snr in [-5, 0, 5, 10]}
    meta_csv_snr = {snr:[] for snr in [-5, 0, 5, 10]}
    i=0
    for index, row in df_clean.iterrows():
        index_noise = i % len(df_noise)
        row_noise = df_noise.iloc[index_noise]
        m_csv, m_json_clean, m_json_noisy, m_csv_snr, m_json_clean_snr, m_json_noisy_snr = generate_mix(row, row_noise, index, sr, snrs[i], args, generate_snrs=True)
        meta_csv.append(m_csv)
        meta_json_clean.append(m_json_clean)
        meta_json_noisy.append(m_json_noisy)
        for snr in [-5, 0, 5, 10]:
            meta_csv_snr[snr].extend(m_csv_snr[snr])
            meta_json_clean_snr[snr].extend(m_json_clean_snr[snr])
            meta_json_noisy_snr[snr].extend(m_json_noisy_snr[snr])
        i += 1
    
    #iterate through dataframes
    meta_json_clean_large = []
    meta_json_noisy_large = []
    meta_csv_large = []
    i=0
    for index, row in df_clean.iterrows():
        for index_noise, row_noise in df_noise.iterrows():
            m_csv, m_json_clean, m_json_noisy, _, _, _ = generate_mix(row, row_noise, i, sr, snrs_large[i], args, generate_snrs=False, suffix='_large')
            meta_csv_large .append(m_csv)
            meta_json_clean_large .append(m_json_clean)
            meta_json_noisy_large .append(m_json_noisy)
            i += 1
    return meta_csv, meta_json_clean, meta_json_noisy, meta_csv_snr, meta_json_clean_snr, meta_json_noisy_snr, meta_csv_large, meta_json_clean_large, meta_json_noisy_large

    
def generate_datasets(args):
    df_clean = pd.read_csv(os.path.join(args.data_dir,'clean.csv'))
    df_noise = pd.read_csv(os.path.join(args.data_dir,'noise.csv'))
    for sr in SAMPLE_RATES:
        os.makedirs(os.path.join(args.data_dir,str(sr),'clean'),exist_ok=True)
        os.makedirs(os.path.join(args.data_dir,str(sr),'noisy'),exist_ok=True)
        os.makedirs(os.path.join(args.data_dir,str(sr),'noise'),exist_ok=True)
        os.makedirs(os.path.join(args.data_dir,str(sr)+'_large','clean'),exist_ok=True)
        os.makedirs(os.path.join(args.data_dir,str(sr)+'_large','noisy'),exist_ok=True)
        os.makedirs(os.path.join(args.data_dir,str(sr)+'_large','noise'),exist_ok=True)
        for snr in [-5, 0, 5, 10]:
            os.makedirs(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'clean'),exist_ok=True)
            os.makedirs(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noisy'),exist_ok=True)
            os.makedirs(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noise'),exist_ok=True)
            
        meta_csv, meta_json_clean, meta_json_noisy, meta_csv_snr, meta_json_clean_snr, meta_json_noisy_snr, meta_csv_large, meta_json_clean_large, meta_json_noisy_large = pair_files(df_clean[df_clean['type']=='terrestrial'],df_noise[df_noise['type']=='terrestrial'],sr,args)
        csv, mclean, mnoisy, csv_snr, mclean_snr, mnoisy_snr, csv_large, mclean_large, mnoisy_large = pair_files(df_clean[df_clean['type']=='underwater'],df_noise[df_noise['type']=='underwater'],sr,args) 

        meta_csv.extend(csv)
        meta_json_clean.extend(mclean)
        meta_json_noisy.extend(mnoisy)
        meta_csv_large.extend(csv_large)
        meta_json_clean_large.extend(mclean_large)
        meta_json_noisy_large.extend(mnoisy_large)
        
        np.savetxt(os.path.join(args.data_dir,str(sr),'metadata.csv'), np.array(meta_csv), delimiter=",", fmt='%s', header='filename,nsamples,sample_rate,snr,clean_filename,noise_filename,type')        
        with open(os.path.join(args.data_dir,str(sr),'clean.json'), 'w', encoding='utf-8') as f:
            json.dump(meta_json_clean, f, ensure_ascii=False, indent=4)
        with open(os.path.join(args.data_dir,str(sr),'noisy.json'), 'w', encoding='utf-8') as f:
            json.dump(meta_json_noisy, f, ensure_ascii=False, indent=4)
        
        np.savetxt(os.path.join(args.data_dir,str(sr)+'_large','metadata.csv'), np.array(meta_csv_large), delimiter=",", fmt='%s', header='filename,nsamples,sample_rate,snr,clean_filename,noise_filename,type')        
        with open(os.path.join(args.data_dir,str(sr)+'_large','clean.json'), 'w', encoding='utf-8') as f:
            json.dump(meta_json_clean, f, ensure_ascii=False, indent=4)
        with open(os.path.join(args.data_dir,str(sr)+'_large','noisy.json'), 'w', encoding='utf-8') as f:
            json.dump(meta_json_noisy, f, ensure_ascii=False, indent=4)
            
        for snr in [-5, 0, 5, 10]:
            meta_csv_snr[snr].extend(csv_snr[snr])
            meta_json_clean_snr[snr].extend(mclean_snr[snr])
            meta_json_noisy_snr[snr].extend(mnoisy_snr[snr])
            
            np.savetxt(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'metadata.csv'), np.array(meta_csv_snr[snr]), delimiter=",", fmt='%s', header='filename,nsamples,sample_rate,snr,clean_filename,noise_filename,type')        
            with open(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'clean.json'), 'w', encoding='utf-8') as f:
                json.dump(meta_json_clean_snr[snr], f, ensure_ascii=False, indent=4)
            with open(os.path.join(args.data_dir,str(sr)+'_snr_experiments',str(snr),'noisy.json'), 'w', encoding='utf-8') as f:
                json.dump(meta_json_noisy_snr[snr], f, ensure_ascii=False, indent=4)
            
    
    
def wavread(path, tag, target_sr):
    '''
    input: path (str)
    output: audio (torch.tensor)
    '''
    ### loading audio
    audio, sr = torchaudio.load(path, normalize=True)
    #audio = (audio - audio.min())/(audio.max() - audio.min() + 1e-9)*2 - 1
    audio = audio/abs(audio).max()

    time_samples = audio.shape[1]   

    ### resampling
    if sr!=target_sr:
        ### for the noise samples of lower sample rate we don't do any stretching and resampling 
        ### we just play the noisy audio faster
        if sr<target_sr and 'noise' not in tag:
            
            # if (sr/target_sr)<0.8:
            #     ratios = torch_time_stretch.get_fast_stretches(sr)
            #     ### compute the closest time stretch ratio
            #     ratio = min(ratios, key=lambda x:abs(x.numerator/x.denominator-sr/target_sr))
            #     audio = torch_time_stretch.time_stretch(audio[None,None,:], ratio, sr)[0,0,:]

            ### resample    
            true_ratio = target_sr/sr
            audio = torchaudio.transforms.Resample(sr, target_sr)(audio)
            
            ### ensure the number of time samples
            expected_time_samples = int(true_ratio * time_samples)
            if audio.shape[1]>expected_time_samples:
                audio = audio[:,:expected_time_samples]
            elif audio.shape[1]<expected_time_samples:
                audio = torch.cat((audio,torch.zeros(1,expected_time_samples-audio.shape[1])), axis=1)
        elif sr>target_sr:
            audio = torchaudio.transforms.Resample(sr, target_sr)(audio)
        
        sr = target_sr 
        
    return audio,sr   

if __name__ == "__main__":
    args = parser.parse_args()
    generate_datasets(args)
