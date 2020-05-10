from random import uniform
from sys import byteorder
from array import array
from struct import pack
from sklearn.preprocessing import LabelEncoder
import pyaudio
import wave
import nn_CNN_recognition as nn
from gevent._compat import xrange
import soundfile as sf
import os
import time
THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100


while(True):

    print("Speech")
    def is_silent(snd_data):
        "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < THRESHOLD


    def normalize(snd_data):
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r


    def trim(snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data


    def add_silence(snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        r = array('h', [0 for i in xrange(int(seconds * RATE))])
        r.extend(snd_data)
        r.extend([0 for i in xrange(int(seconds * RATE))])
        return r


    def record():
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=1, rate=RATE,
                        input=True, output=True,
                        frames_per_buffer=CHUNK_SIZE)

        num_silent = 0
        snd_started = False

        r = array('h')

        while 1:
            # little endian, signed short
            snd_data = array('h', stream.read(CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)
            silent = is_silent(snd_data)
            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 20:     #30
                break

        sample_width = p.get_sample_size(FORMAT)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = normalize(r)
        r = trim(r)
        r = add_silence(r, 0.25)
        return sample_width, r


    def record_to_file(path):
        "Records from the microphone and outputs the resulting data to 'path'"
        sample_width, data = record()
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()

    def convet_wav_to_ogg():
        path = 'Record_test'

        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.wav' in file:
                    files.append(os.path.join(r, file))

        for f in files:
            data, samplerate = sf.read(f)
            sf.write(f + '.ogg', data, samplerate)
            #print(f)

    if __name__ == '__main__':
        le_test = LabelEncoder()
        #1: back 2:left 3:right 4:stop 5:up 6:unknow
        le_test.fit([1, 2, 3, 4, 5, 6])
        print("please speak a word into the microphone")
        a = uniform(1.0,10.0)
        path_file='Record_test/demo'+str(a)+'.ogg'
        record_to_file(path_file)
        #convet_wav_to_ogg()
        start = time.time()
        nn.predict(path_file, le_test, "trained_cnn.h5")
        print("done - result written to demo.wav")
        print(time.time()-start)
