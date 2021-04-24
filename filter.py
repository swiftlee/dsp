from audio import Audio
import matplotlib.pyplot as plt
from scipy.signal import freqz
import numpy as np
import utility
from pydub import AudioSegment

thistle = Audio("thistle.wav")

instruments = {
  "dbl_bass": [20.0, 13959.0],
  "cellos": [40.0, 9825.0],
  "violas": [100.0, 10000.0],
  "violins": [140.0, 23450.0],
}

order = 5

#bandpass double bass 0 hz to 13959 hz
#bandpass celli 40 hz to 9825 hz
#bandpass violas 100 hz to 10000 hz
#bandpass violins 140 hz to 30000 hz

for section, freqz in instruments.items():
  print(f"Filtering {section}... from {freqz[0]} Hz -> {freqz[1]}")
  thistle.filter_wav(*freqz, section, order)
print("Done filtering!!!")


# PANNING CODE
# filtered_thistle = AudioSegment.from_wav("thistle-filtered.wav")
# filtered_thistle = filtered_thistle.pan(-1)
# filtered_thistle.export("thistle-panned.wav", format="wav")
