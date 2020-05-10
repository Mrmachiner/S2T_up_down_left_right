# script takes a .ogg file as input and converts it into .wav form. This .wav file can be played using MP3 player.
# The waveform is visualized in the form of a plot.
# python visualize_data.py -o "dataset/001 - Dog bark/1-30226-A.ogg"
import glob
from random import uniform

import matplotlib.pyplot as plt
import numpy as np
import wave
import soundfile as sf
import sys
import os
import argparse


def visualize_wav(oggfile,number):
    data, samplerate = sf.read(oggfile)

    if not os.path.exists('sample_wav'):
        os.mkdir('sample_wav')

    sf.write('sample_wav/new_file_Fire.wav', data, samplerate)
    spf = wave.open('sample_wav/new_file_Fire.wav')
    signal = spf.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    if spf.getnchannels() == 2:
        print('just mono files. not stereo')
        sys.exit(0)

    # plotting x axis in seconds. create time vector spaced linearly with size of audio file. divide size of signal by frame rate to get stop limit
    Time = np.linspace(0, len(signal) / samplerate, num=len(signal))
    plt.figure(1)
    plt.title('Signal Wave Vs Time(in sec)')
    plt.plot(Time, signal)
    plt.savefig('sample_wav/sample_waveplot_Fire'+str(number)+'.png', bbox_inches='tight')
    plt.show()


def read(path):
    files=[]
    for r, d, f in os.walk(path):
        for file in f:
            if '.wav' in file:
                files.append(os.path.join(r, file))


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    #parser.add_argument('-o', '--ogg_file', help='Relative path to a .ogg file',default='test/back/demo9.484276840927278.wav.ogg')
    #args = parser.parse_args()
    for file_name in glob.glob(os.path.join('test/back', "*.ogg")):
        number = uniform(1.0, 10.0)
        print("Extracting file ", file_name)
        visualize_wav(file_name,number)

