#!/usr/bin/env python3
from pydub import AudioSegment
import sys
import os
def detect_leading_silence(sound, silence_threshold=-30.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms
def trim_file(i,o):
    sound = AudioSegment.from_file(i, format="aac")

    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)    
    trimmed_sound = sound[start_trim:duration-end_trim]
    trimmed_sound.export(o,format='adts')

argv = sys.argv
if(len(argv) < 2):
    print('default dir')
    d = '.'
else:
    d = argv[1]
if(not d.endswith('/')):
    d += '/' 
dirs = os.listdir(d)
for di in dirs:
    ori = d + '%s/original/' % (di)
    trim = d + '%s/trim/' % (di)
    try:
        os.mkdir(trim)
    except:
        pass
    try:
        files = [i for i in os.listdir(ori) if i.endswith('.aac')]
    except:
        exit()
    for f in files:
        print(f)
        trim_file(ori + f, trim + f)
