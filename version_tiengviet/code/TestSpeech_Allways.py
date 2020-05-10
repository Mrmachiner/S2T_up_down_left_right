
#Check_Sound import
from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from gevent._compat import xrange

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
#End Check_Sound import

#Check_Sound Code
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




def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in xrange(int(seconds * RATE))])
    r.extend(snd_data)
    r.extend([0 for i in xrange(int(seconds * RATE))])
    return r


def record():
    print("Da Vao Record")
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

        if snd_started and num_silent > 100:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    #r = trim(r)
    r = add_silence(r, 0.5)
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

#End Check_Sound Code

import websocket
import socket
REMOTE_SERVER = "www.google.com"

def is_connected():
  try:
    host = socket.gethostbyname(REMOTE_SERVER)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False
while(True):
    if(is_connected()):
        import speech_recognition
        import time

        trigger_up = "tiến lên"
        trigger_up1 = "tiến"

        trigger_down = "lùi lại"
        trigger_down1 = "lùi"

        trigger_left = "sang trái"
        trigger_left1 = "trái"
        trigger_left2 = "rẽ trái"

        trigger_right = "sang phải"
        trigger_right1 = "rẽ phải"
        trigger_right2 = "phải"

        trigger_stop1 = "dừng"
        trigger_stop = "dừng lại"
        key = "Ok Google"

        recognizer = speech_recognition.Recognizer()

        print("Beginning to listen...")


        def listen():
            start = time.time()
            with speech_recognition.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, phrase_time_limit=2)
                # print(audio)
            try:
                print(recognizer.recognize_google(audio, language='vi-VN'))
                text = recognizer.recognize_google(audio, language='vi-VN')
                print("true")
                print((time.time() - start))
                # print(text)
                return text
            except speech_recognition.UnknownValueError:
                print("Could not understand audio")
            print(time.time() - start)
            return ""


        print("Trying to always listen...")

        while 1:
            sample_width, data = record()
            if(data!=''):
                list = listen()
                if list == trigger_up or list == trigger_up1:
                    print("Len")
                elif list == trigger_down or list == trigger_down1:
                    print("Xuong")
                elif list == trigger_left or list == trigger_left1 or list == trigger_left2:
                    print("Trai")
                    print("Phai")
                elif list == trigger_stop or list == trigger_stop1:
                    print("Dung")
                time.sleep(1)

    else:
        print("Disconnect")