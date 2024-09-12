import os 
import argparse
import pandas as pd 
import numpy as np
import librosa
import soundfile as sf
import json

EXCLUDE = ['bl36or46_pi82ye52_August_05_2023_33646121.wav','bl36or46_pi82ye52_August_05_2023_33646121.wav','bl28gr14_pi171gy171_July_13_2023_35333869.wav','bl28gr14_pi171gy171_July_13_2023_35333869.wav','bl22gr2_bl39gr19_July_06_2023_36711231.wav','bl22gr2_bl39gr19_July_06_2023_36711231.wav','ye56gr26_ye54gr24_June_22_2023_54030487.wav','ye56gr26_ye54gr24_June_20_2023_72647539.wav','ye56gr26_ye54gr24_June_22_2023_54030487.wav','ye56gr26_ye54gr24_June_20_2023_72647539.wav','bl39gr19_bl35or45_June_06_2023_72861961.wav','bl39gr19_bl35or45_June_06_2023_72861961.wav','bl138gr58_ye7gr17_March_23_2023_76747279.wav','bl138gr58_ye7gr17_March_23_2023_76747279.wav','ye56gr26_ye54gr24_June_20_2023_72186361.wav','ye7gr17_bl137or47_June_17_2023_28148961.wav','ye7gr17_bl39gr19_July_29_2023_30221449.wav','pi82ye52_bl51gr31_July_19_2023_28028706.wav','pi82ye52_bl51gr31_July_18_2023_36337868.wav','gr86pi76_bl138gr58_April_12_2023_75899781.wav','gr25pi85_gr27pi87_July_11_2023_58278705.wav','gr25pi85_bl54gr34_October_02_2023_45300000.wav','gr20pi170_bl54gr34_July_15_2023_50429180.wav','bl138gr58_bl53gr33_October_04_2023_73680000.wav','bl138gr58_bl53gr33_October_03_2023_75090000.wav','bl138gr38_bl54gr34_October_28_2023_34020000.wav','gr20pi170_bl36or46_June_28_2023_27359467.wav','bl138gr58_ye7gr17_March_22_2023_75156387.wav','bl138gr58_gr27pi87_July_01_2023_32971014.wav','bl138gr58_bl53gr33_October_04_2023_74220000.wav','bl138gr58_bl53gr33_October_03_2023_74310000.wav','bl138gr38_bl54gr34_October_28_2023_32550000.wav','bl54gr34_ye7gr17_June_29_2023_63484305.wav','bl54gr34_ye7gr17_June_28_2023_62988458.wav','bl54gr34_bl138gr58_October_10_2023_68700000.wav','bl53gr33_bl22gr2_October_21_2023_42720000.wav','bl39gr19_bl35or45_June_06_2023_66964087.wav','bl35or45_gr20pi170_July_25_2023_26488531.wav','bl22gr2_bl39gr19_July_07_2023_31837287.wav','bl22gr2_bl39gr19_July_06_2023_33251372.wav','bl22gr2_bl52gr32_June_24_2023_32909932.wav','ye7gr17_bl39gr19_July_29_2023_19644335.wav','gr25pi85_bl54gr34_October_01_2023_39270000.wav','gr20pi190_gr20pi170_August_01_2023_31671789.wav','bl138gr58_bl53gr33_October_03_2023_74310000.wav','bl54gr34_bl138gr58_October_10_2023_68700000.wav','bl53gr33_bl22gr2_October_21_2023_42720000.wav','ye56gr26_ye54gr24_June_22_2023_61805516.wav','ye7gr17_bl36or46_September_04_2023_69555840.wav','gr86pi76_ye54gr24_July_20_2023_46528689.wav','gr25pi85_bl54gr34_October_01_2023_65130000.wav','gr20pi190_ye56gr26_June_16_2023_24906261.wav','bl138gr58_gr27pi87_July_01_2023_70836327.wav','bl54gr34_ye7gr17_June_30_2023_27460828.wav','ye7gr17_bl39gr19_July_28_2023_67032449.wav','bl53gr33_bl22gr2_October_22_2023_43620000.wav','bl22gr2_bl52gr32_June_24_2023_32909932.wav','ye56gr26_ye54gr24_June_21_2023_69517662.wav','ye7gr17_bl36or46_September_05_2023_34788718.wav','bl138gr58_ye7gr17_March_22_2023_75156387.wav','bl138gr58_bl53gr33_October_04_2023_75120000.wav','bl54gr34_ye7gr17_June_29_2023_31285592.wav','bl51gr31_pi171gy171_July_26_2023_65118258.wav','bl36or46_bl53gr33_June_12_2023_41565241.wav','bl22gr2_gr20pi190_September_29_2023_73500000.wav','bl22gr2_bl39gr19_July_06_2023_46729255.wav','bl22gr2_bl52gr32_June_26_2023_36936347.wav','bl138gr58_ye7gr17_March_23_2023_75956344.wav','ye7gr17_bl35or45_July_04_2023_56777962.wav','ye56gr26_ye54gr24_June_21_2023_74329420.wav']
ON = 0.01
OFF = 0.03

def download_samples(local_path):
    # Download annotations from the the gcp address using gsutil 
    for i in range(1, 34):
        os.makedirs(os.path.join(local_path, 'Pair'+str(i)), exist_ok=True)
        os.system('gsutil -m cp -r gs://zebra_finch_interactive_playbacks/data/natural_0000/Pair'+str(i)+'/voxaboxen_mixit_test '+os.path.join(local_path,'Pair'+str(i)))
        os.system('gsutil -m cp -r gs://zebra_finch_interactive_playbacks/data/natural_0000/Pair'+str(i)+'/Stereo_selection_tables '+os.path.join(local_path,'Pair'+str(i)))
            
        files = sorted([file for file in os.listdir(os.path.join(local_path, 'Pair'+str(i), "voxaboxen_mixit_test")) if file.endswith('.wav') and not file.startswith('.')])

        os.makedirs(os.path.join(local_path, 'Pair'+str(i),'Stereo'), exist_ok=True)
        # os.makedirs(os.path.join(local_path, 'Pair'+str(i),'separation'), exist_ok=True)
        for file in files:
            os.system('gsutil cp gs://zebra_finch_interactive_playbacks/data/natural_0000/Pair'+str(i)+'/Stereo/'+file+' '+os.path.join(local_path,'Pair'+str(i),'Stereo'))

def download_noise(local_path,files,i):
    for file in files:
        os.system('gsutil cp gs://zebra_finch_interactive_playbacks/data/natural_0000/Pair'+str(i)+'/Stereo/'+file+' '+os.path.join(local_path,'Pair'+str(i),'Stereo'))

def is_silent(local_path,file,i):
    csv_path = os.path.join(local_path,'Pair'+str(i), "Stereo_selection_tables", file) 
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, sep='\t')
        if len(df) == 0:
            return True
    return False
    
    
def process_with_extra_noise(local_path,output_path,file,noise_file,i,sr):
    noise_stereo,sr = librosa.load(os.path.join(local_path,'Pair'+str(i),'Stereo',noise_file),sr=sr)
    clean_stereo,sr = librosa.load(os.path.join(local_path,'Pair'+str(i),'voxaboxen_mixit_test',file),sr=sr)

    
    clean_mono = librosa.to_mono(clean_stereo)
    noise_mono = librosa.to_mono(noise_stereo)
    if len(clean_mono) > len(noise_mono):
        clean_mono = clean_mono[:len(noise_mono)]
    elif len(clean_mono) < len(noise_mono):
        clean_mono = np.pad(clean_mono, (0,len(noise_mono)-len(clean_mono)))
    noisy_mono = clean_mono + noise_mono
    
    filename = file.replace('.wav','')+ '_' + noise_file
    
    sf.write(os.path.join(output_path,str(sr),'noisy',filename), noisy_mono, sr)
    sf.write(os.path.join(output_path,str(sr),'clean',filename), clean_mono, sr)
    sf.write(os.path.join(output_path,str(sr),'noise',filename), noise_mono, sr)
    
    return [os.path.join(output_path,str(sr),'noisy',filename), len(noisy_mono)],[os.path.join(output_path,str(sr),'clean',filename), len(clean_mono)], [os.path.join(output_path,str(sr),'noise',filename), len(noise_mono)]


def process(local_path,output_path,file,filenoise,i,sr,small_set,rngnp):
    left = file.split('_')[0]
    right = file.split('_')[1]
    timestamp = file.split('_',2)[2].split('.')[0]
    
    noisy_stereo,sr = librosa.load(os.path.join(local_path,'Pair'+str(i),'Stereo',file),sr=sr)
    clean_stereo,sr = librosa.load(os.path.join(local_path,'Pair'+str(i),'voxaboxen_mixit_test',file),sr=sr)
    noise_stereo = noisy_stereo - clean_stereo
    
    csv_path = os.path.join(local_path,'Pair'+str(i), "Stereo_selection_tables", 'peaks_pred_'+file.replace('.wav','.txt'))

    df = pd.read_csv(csv_path, sep='\t')

    #### load the detection
    timestamps_sec = [[],[]]
    timestamps_all = []
    for c,channel in enumerate(['Left', 'Right']):
        dfc = df[df['Annotation']==channel]
        for i in range(len(dfc)):
            idx = dfc.index[i]
            timestamps_sec[c].append([np.maximum(0,dfc['Begin Time (s)'].iloc[i]-ON),dfc['End Time (s)'].iloc[i]+OFF])
            timestamps_all.append([np.maximum(0,dfc['Begin Time (s)'].iloc[i]-ON),dfc['End Time (s)'].iloc[i]+OFF])

    #### sort and merge timestamps_all
    timestamps_all = sorted(timestamps_all, key=lambda x: x[0])
    i = 0
    while i < len(timestamps_all)-1:
        if timestamps_all[i][1] > timestamps_all[i+1][0]:
            timestamps_all[i][1] = timestamps_all[i+1][1]
            timestamps_all.pop(i+1)
        i += 1
    

    noise_frames = []
    durations = []
    for j in range(len(timestamps_all)):
        start_frame = 0 if j == 0 else int(timestamps_all[j-1][1] * sr)
        end_frame =  np.minimum(noisy_stereo.shape[-1],int(timestamps_all[j][0] * sr))
        if end_frame - start_frame>0:
            overlaps = False
            for _,ts in enumerate(timestamps_all):
                    if (start_frame < ts[1]*sr) and (end_frame > ts[0]*sr):
                        overlaps = True
                        break
            if not overlaps:
                noise_frames.append([start_frame,end_frame])
                durations.append(end_frame - start_frame)
        # else:
        #     import pdb; pdb.set_trace()
    start_frame = int(timestamps_all[-1][1] * sr)
    end_frame = noisy_stereo.shape[-1]
    overlaps = False
    if end_frame - start_frame>0:
        for _,ts in enumerate(timestamps_all):
                if (start_frame < ts[1]*sr) and (end_frame > ts[0]*sr):
                    overlaps = True
                    break
        if not overlaps:
            noise_frames.append([start_frame,end_frame])
            durations.append(end_frame - start_frame)
                
    # max_duration_id = np.argmax(durations)
    # start_frame_noise = np.maximum(1024,noise_frames[max_duration_id][0])
    # end_frame_noise = np.minimum(noisy_stereo.shape[-1]-1024,noise_frames[max_duration_id][1])
    # duration_noise = end_frame_noise - start_frame_noise
    # import pdb; pdb.set_trace()    

    write_files = True
    if len(durations) > 0:
        noisy_mono = librosa.to_mono(noisy_stereo)
        clean_mono = librosa.to_mono(clean_stereo)
        noise_mono = librosa.to_mono(noise_stereo)
        for c,ts in enumerate(timestamps_sec):
            for start, end in ts:
                #### convert from time to samples
                start_frame = int(start * sr)
                end_frame =  np.minimum(noisy_stereo.shape[-1],int(end * sr))
                duration = end_frame - start_frame
                
                possible_noises = [duration_id for duration_id, duration_n in enumerate(durations) if duration_n > duration]
                # print(len(possible_noises))
                if len(possible_noises) > 0:
                    chosen_noise = rngnp.choice(possible_noises)    
                    start_frame_noise = np.maximum(1024,noise_frames[chosen_noise][0])
                    end_frame_noise = np.minimum(noisy_stereo.shape[-1]-1024,noise_frames[chosen_noise][1])
                    duration_noise = end_frame_noise - start_frame_noise
                    
                    if (duration_noise-2048) > duration:
                        start_noise_here = rngnp.integers(start_frame_noise, end_frame_noise-duration-2048)
                    else:
                        start_noise_here = start_frame_noise
                                    
                    #### take the overlapping part and multiply with the window
                    wsize = np.minimum(1024, start_frame-1024)
                    if wsize > 0:
                        ### hanning window
                        ramp = np.linspace(0, 1, wsize)
                        inv_ramp = np.flip(ramp)
                        noise_mono[start_frame-wsize:start_frame] = noise_mono[start_frame-wsize:start_frame] * inv_ramp
                        noise_mono[start_frame-wsize:start_frame] += noise_mono[start_noise_here:start_noise_here+wsize] * ramp
                        
                    #### add the noise
                    noise_mono[start_frame:end_frame] = noise_mono[start_noise_here+wsize:start_noise_here+wsize+duration]

                    #### take the overlapping part and multiply with the window
                    wsize = np.minimum(1024, noisy_stereo.shape[-1]-end_frame-1024)
                    if wsize > 0:
                        ramp = np.linspace(0, 1, wsize)
                        inv_ramp = np.flip(ramp)
                        noise_mono[end_frame:end_frame+wsize] = noise_mono[end_frame:end_frame+wsize] * ramp
                        noise_mono[end_frame:end_frame+wsize] += noise_mono[start_noise_here+duration+wsize:start_noise_here+duration+2*wsize] * inv_ramp
                else:
                    write_files = False
                    break        
        noisy_mono = clean_mono + noise_mono
    else:
        write_files = False    
        
    if write_files:
        # sf.write(os.path.join(output_path,str(sr)+'_large','noisy',file), noisy_mono, sr)
        # sf.write(os.path.join(output_path,str(sr)+'_large','clean',file), clean_mono, sr)
        # sf.write(os.path.join(output_path,str(sr)+'_large','noise',file), noise_mono, sr)
        
        if small_set:
            sf.write(os.path.join(output_path,str(sr),'noisy',file), noisy_mono, sr)
            sf.write(os.path.join(output_path,str(sr),'clean',file), clean_mono, sr)
            sf.write(os.path.join(output_path,str(sr),'noise',file), noise_mono, sr)

            assert os.path.exists(os.path.join(output_path,str(sr),'noisy',file))
            assert os.path.exists(os.path.join(output_path,str(sr),'clean',file))
            assert os.path.exists(os.path.join(output_path,str(sr),'noise',file))
        return [os.path.join(output_path,str(sr)+'_large','noisy',file), len(noisy_mono)],[os.path.join(output_path,str(sr)+'_large','clean',file), len(clean_mono)], [os.path.join(output_path,str(sr)+'_large','noise',file), len(noise_mono)]
    else:
        print('No noise found in file: ', file)
        return [None, None],[None, None], [None, None]         
        
        
        
def __main__():
    parser = argparse.ArgumentParser(description='Download zebra finch annotations')
    parser.add_argument('--local_path', type=str, help='Local path to save the annotations')
    parser.add_argument('--out_path', type=str, help='Local path to save the resulting dataset')
    args = parser.parse_args()
    # arg_dic = dict(vars(args))
    # rngnp = np.random.default_rng(seed=42)
    
    # download_samples(args.local_path)
    
    if os.path.exists(os.path.join(args.out_path,'16000','metadata.csv')):
        print('Files already exist, cleaning ...')
        for sr in [16000,48000]:
            df = pd.read_csv(os.path.join(args.out_path,'16000','metadata.csv'),header=None)
            files = df[df[1]==False][0].values
            files_clean = df[df[1]==True][0].values
            print("Removing files: ", files)
            print("Total files: ", len(df))
            noisy = json.load(open(os.path.join(args.out_path,str(sr),'noisy.json')))
            print("Total files: ", len(noisy))
            clean = json.load(open(os.path.join(args.out_path,str(sr),'clean.json')))
            noise = json.load(open(os.path.join(args.out_path,str(sr),'noise.json')))
            for file in files:
                filename = os.path.basename(file)
                # ## remove file
                if os.path.exists(os.path.join(args.out_path,str(sr),'noisy',filename)):
                    os.remove(os.path.join(args.out_path,str(sr),'noisy',filename))
                if os.path.exists(os.path.join(args.out_path,str(sr),'clean',filename)):
                    os.remove(os.path.join(args.out_path,str(sr),'clean',filename))
                if os.path.exists(os.path.join(args.out_path,str(sr),'noise',filename)):
                    os.remove(os.path.join(args.out_path,str(sr),'noise',filename))
                ## remove from json
                idx =  [i for i,k in enumerate(noisy) if noisy[i][0].endswith(filename)] 
                if len(idx) > 0:
                    noisy.pop(idx[0])
                idx =  [i for i,k in enumerate(clean) if clean[i][0].endswith(filename)] 
                if len(idx) > 0:
                    clean.pop(idx[0])
                idx =  [i for i,k in enumerate(noise) if noise[i][0].endswith(filename)] 
                if len(idx) > 0:
                    noise.pop(idx[0])
            print("Total files after cleaning: ", len(noisy))
            json.dump(noisy, open(os.path.join(args.out_path,str(sr),'noisy.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            json.dump(clean, open(os.path.join(args.out_path,str(sr),'clean.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
            json.dump(noise, open(os.path.join(args.out_path,str(sr),'noise.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


    
    else:
    
        os.makedirs(args.out_path, exist_ok=True)
        print('Creating dataset ...')
        for sr in [16000,48000]:
            os.makedirs(os.path.join(args.out_path,str(sr),'noisy'), exist_ok=True)
            os.makedirs(os.path.join(args.out_path,str(sr),'clean'), exist_ok=True)
            os.makedirs(os.path.join(args.out_path,str(sr),'noise'), exist_ok=True)
            # os.makedirs(os.path.join(args.out_path,str(sr)+'_large','noisy'), exist_ok=True)
            # os.makedirs(os.path.join(args.out_path,str(sr)+'_large','clean'), exist_ok=True)
            # os.makedirs(os.path.join(args.out_path,str(sr)+'_large','noise'), exist_ok=True)
        
        noisy_list={16000:[],48000:[]}
        clean_list={16000:[],48000:[]}
        noise_list={16000:[],48000:[]}
        noisy_list_small={16000:[],48000:[]}
        clean_list_small={16000:[],48000:[]}
        noise_list_small={16000:[],48000:[]}
            
        for i in range(1, 34):
            files = sorted([file for file in os.listdir(os.path.join(args.local_path, 'Pair'+str(i), "voxaboxen_mixit_test")) if file.endswith('.wav') and not file.startswith('.') and file not in EXCLUDE])
            assert len(files) > 0, "No files found in Pair{}".format(i)
            rngnp = np.random.default_rng(seed=42)
        
            smallset_files = rngnp.choice(files, 2, replace=False)
            # while smallset_files[0] in EXCLUDE:
            #     smallset_files = rngnp.choice(files, 1, replace=False)
                
            # smallset_files = [files[len(files)//2]]
            # annotations = sorted([file for file in os.listdir(os.path.join(args.local_path, 'Pair'+str(i), "Stereo_selection_tables")) if file.endswith('.txt') and not file.startswith('.')])
            # silent_files = [file.replace('peaks_pred_','').replace('.txt','.wav') for file in annotations if is_silent(args.local_path,file,i)]

            # noise_files = [rngnp.choice(silent_files) for file in files]
            # noise_files_small = [file for file in smallset_files if file in silent_files]
            noise_files_small = smallset_files
            noise_files = files
            # download_noise(args.local_path,noise_files,i)
            # import pdb; pdb.set_trace()
            #for file,noise_file in zip(files,noise_files):
            
            for sr in [16000,48000]:
                
                for file,noise_file in zip(smallset_files,noise_files_small):
                    small_set = file in smallset_files
                    small_set = True
                    noisy,clean,noise = process(args.local_path,args.out_path,file,noise_file,i,sr,small_set,rngnp)
                    if noise[0] is not None:
                        noisy_list[sr].append((noisy[0],noisy[1]))
                        clean_list[sr].append((clean[0],clean[1]))
                        noise_list[sr].append((noise[0],noise[1]))
                        if small_set:
                            noisy[0] = noisy[0].replace('_large','')
                            clean[0] = clean[0].replace('_large','')
                            noise[0] = noise[0].replace('_large','')
                            noisy_list_small[sr].append((noisy[0],noisy[1]))
                            clean_list_small[sr].append((clean[0],clean[1]))
                            noise_list_small[sr].append((noise[0],noise[1]))
                        
                ### Write the lists to a json file
                # with open(os.path.join(args.out_path,str(sr)+'_large','noisy.json'), 'w') as f:
                #     json.dump(noisy_list, f)
                # with open(os.path.join(args.out_path,str(sr)+'_large','clean.json'), 'w') as f:
                #     json.dump(clean_list, f)
                # with open(os.path.join(args.out_path,str(sr)+'_large','noise.json'), 'w') as f:
                #     json.dump(noise_list, f)
                with open(os.path.join(args.out_path,str(sr),'noisy.json'), 'w',encoding='utf-8') as f:
                    json.dump(noisy_list_small[sr], f, ensure_ascii=False, indent=4)
                with open(os.path.join(args.out_path,str(sr),'clean.json'), 'w',encoding='utf-8') as f:
                    json.dump(clean_list_small[sr], f, ensure_ascii=False, indent=4)
                with open(os.path.join(args.out_path,str(sr),'noise.json'), 'w',encoding='utf-8') as f:
                    json.dump(noise_list_small[sr], f, ensure_ascii=False, indent=4)
                    
                ### write csv for the small set
                with open(os.path.join(args.out_path,str(sr),'metadata.csv'), 'w') as f:
                    for item in noisy_list[sr]:
                        f.write("%s,%s\n" % (item[0],True))
                        
        

if __name__ == '__main__':
    __main__()