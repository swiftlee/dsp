import os
from scipy import signal
from scipy.io import wavfile, loadmat
import matplotlib.pyplot as plot
import numpy as np
import utility
from pydub import AudioSegment as aus
from progress.bar import Bar


def do_shit(sound):
    samplerate, data = wavfile.read(sound)
    left_channel = data[:, 0]  # get all rows in column 0 (left channel)
    right_channel = data[:, 1]  # get all rows in column 1 (right channel)


claps = "claps.wav"
claps1 = "claps1.wav"
claps2 = "claps2.wav"
claps3 = "claps3.wav"
claps4 = "claps4.wav"
claps5 = "clap5.wav"
claps6 = "claps6.wav"
claps7 = "claps7.wav"
claps8 = "claps8.wav"

# find max of both sounds and subtract them for signal onset shit -- have to explain we used the max instead of signal onset