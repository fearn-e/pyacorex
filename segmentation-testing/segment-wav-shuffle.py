#!/usr/bin/env python3

import pydub

import random

import sys

from pydub import AudioSegment

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

with open(sys.argv[1], 'rb') as f:
    audio = AudioSegment.from_file(f)
    segments = []
    for i in range(0, len(audio), 125):
        segments.append(audio[i:i+125])
    random.shuffle(segments)
    result = segments[0]
    for segment in segments[1:]:
        result += segment
    result.export('shuffled.wav', format='wav')