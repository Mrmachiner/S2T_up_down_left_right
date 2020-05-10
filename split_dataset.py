"""Splits the google speech commands into train, validation and test sets.
"""

import os
import shutil
import argparse
import glob
import soundfile as sf

path = 'test/back'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.mp3' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)

for f in files:
    data, samplerate = sf.read(f)
    sf.write(f+'.ogg', data, samplerate)
    print(f)