''' 
A script to read stem_judgments_full.csv from the input_path argument with the fields Trial,File,MainSource,Source0,Source1,Source2,Source3,MainStillNoisy,OriginalQuietBackgorund,NoVoxAtClipCenter.
Then read the audio with the file name File and if not MainStillNoisy write it to the output_path argument.
'''
import argparse
import os
import pandas as pd
import soundfile as sf
import librosa 
import json
import noisereduce as nr

sampleRates = [16000,48000]

def process_files(input_path, output_path):
    # Read the CSV file
    df = pd.read_csv(input_path, usecols=['Trial','File','MainSource','Source0','Source1','Source2','Source3','MainStillNoisy','OriginalQuietBackgorund','NoVoxAtClipCenter','Selected'])

    for sr in sampleRates:
        noisy_list=[]
        clean_list=[]
        noise_list=[]
        
        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            # If the MainStillNoisy field is not True
            if row['Selected'] and not row['MainStillNoisy'] and not row['NoVoxAtClipCenter'] and not row['OriginalQuietBackgorund']:
                # Read the audio file
                data, samplerate = librosa.load(os.path.join(os.path.dirname(input_path),row['File']),sr=sr)
                stem_id = int(row['MainSource'])
                separated, samplerate_sep = librosa.load(os.path.join(os.path.dirname(input_path),row['File'].replace('.wav','_source'+str(stem_id)+'.wav')), sr=sr)   
                # separated = nr.reduce_noise(y=separated, sr=samplerate, stationary=False)
                noise = None
                for j in range(4):
                    if j != stem_id and not row['Source'+str(j)]:
                        noise1, samplerate_noise = librosa.load(os.path.join(os.path.dirname(input_path),row['File'].replace('.wav','_source'+str(j)+'.wav')), sr=sr)
                        noise = noise1 if noise is None else noise + noise1
                if noise is not None:
                    # Write the audio file to the output path
                    sf.write(os.path.join(output_path,str(sr),'noisy',row['File']), data, sr)
                    sf.write(os.path.join(output_path,str(sr),'clean',row['File']), separated, sr)
                    sf.write(os.path.join(output_path,str(sr),'noise',row['File']), noise, sr)
                    noisy_list.append([os.path.join(output_path,str(sr),'noisy',row['File']), len(data)])
                    clean_list.append([os.path.join(output_path,str(sr),'clean',row['File']), len(separated)])  
                    noise_list.append([os.path.join(output_path,str(sr),'noise',row['File']), len(noise)])
                
    
        ### Write the lists to a json file
        with open(os.path.join(output_path,str(sr),'noisy.json'), 'w') as f:
            json.dump(noisy_list, f)
        with open(os.path.join(output_path,str(sr),'clean.json'), 'w') as f:
            json.dump(clean_list, f)
        with open(os.path.join(output_path,str(sr),'noise.json'), 'w') as f:
            json.dump(noise_list, f)
        
#### main function parsing arguments and iterating over the files

def main():
    parser = argparse.ArgumentParser(description='Read stem_judgments_full.csv and write the audio files that are not MainStillNoisy to the output path')
    parser.add_argument('input_path', type=str, help='The path to the input file')
    args = parser.parse_args()
    
    for sr in sampleRates:
        os.makedirs(os.path.join(args.input_path,str(sr),'noisy'), exist_ok=True)
        os.makedirs(os.path.join(args.input_path,str(sr),'clean'), exist_ok=True)
        os.makedirs(os.path.join(args.input_path,str(sr),'noise'), exist_ok=True)
    
    process_files(os.path.join(args.input_path,'carrion_crows_mixit','stem_judgments_full.csv'), args.input_path)
    
if __name__ == "__main__":
    main()
    
# python carrioncrows.py /home/marius/data/carrion_crows_denoising