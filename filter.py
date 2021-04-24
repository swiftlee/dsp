from audio import Audio
import matplotlib.pyplot as plt
from scipy.signal import freqz
import numpy as np
import utility
from pydub import AudioSegment

thistle = Audio("thistle.wav")

low_stop = 500.0
high_stop = 1250.0
order = 5

filtered_left = thistle.bandpass_filter(thistle.left_channel, low_stop, high_stop, 5)
filtered_right = thistle.bandpass_filter(thistle.right_channel, low_stop, high_stop, 5)
filtered_result = [0, 0]
filtered_result[0] = filtered_left
filtered_result[1] = filtered_right
normalized = utility.pcm2float(np.asarray(filtered_result).T.astype("int16"), "float32")
soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")
thistle.write_result('thistle-filtered.wav', utility.float2pcm(soundToPlay.T))

filtered_thistle = AudioSegment.from_wav("thistle-filtered.wav")
filtered_thistle = filtered_thistle.pan(-1)
filtered_thistle.export("thistle-panned.wav", format="wav")


