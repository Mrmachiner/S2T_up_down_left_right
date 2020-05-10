import os
import librosa
import soundfile as sf
import numpy as np
import glob
import pandas as pd

def get_features(file_name):

    if file_name: 
        X, sample_rate = sf.read(file_name, dtype='float32')

    f = open("abdc.txt", "w")
    for item in X:
        f.write("%s\n" % item)
    print("Day la get features X", X)
    print("Day la get features sample_rate", sample_rate)
    # mfcc (mel-frequency cepstrum)
    mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
    mfccs_scaled = np.mean(mfccs.T,axis=0)
    return mfccs_scaled

def extract_features():
    # path to dataset containing 10 subdirectories of .ogg files
    sub_dirs = os.listdir('File_Check')
    sub_dirs.sort()
    features_list = []
    for label, sub_dir in enumerate(sub_dirs):  
        for file_name in glob.glob(os.path.join('File_Check',sub_dir,"*.ogg")):
            print("Extracting file ", file_name)
            try:
                mfccs = get_features(file_name)
                print("Day la mfccs",mfccs)
            except Exception as e:
                print("Extraction error")
                continue
            features_list.append([mfccs,label])

    features_df = pd.DataFrame(features_list,columns = ['feature','class_label'])
    print(features_df.head())
    return features_df
