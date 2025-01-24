#!/usr/bin/env python3

import pydub

import sys

from pydub import AudioSegment

if len(sys.argv) < 2:
    print(f'Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

with open(sys.argv[1], 'rb') as f:
    audio = AudioSegment.from_file(f)
    segments = []
    loudness = []
    for i in range(0, len(audio), 125):
        segments.append(audio[i:i+125])
        loudness.append(segments[-1].dBFS)
    for i in range(1, len(segments)):
        j = i
        while j > 0 and loudness[j] > loudness[j-1]:
            loudness[j], loudness[j-1] = loudness[j-1], loudness[j]
            segments[j], segments[j-1] = segments[j-1], segments[j]
            j -= 1
    result = segments[0]
    for segment in segments[1:]:
        result += segment
    result.export('loudsort.wav', format='wav')