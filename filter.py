from audio import Audio
import matplotlib.pyplot as plt
from scipy.signal import freqz
import numpy as np
import utility

thistle = Audio("thistle.wav")

instruments = {
  "dbl_bass": { "freqz": [20.0, 13959.0], "pan": 0.1 },
  "cellos": {"freqz": [40.0, 9825.0], "pan": 1},
  "violas": {"freqz": [100.0, 10000.0], "pan": -1},
  "violins":{"freqz": [140.0, 23450.0], "pan": -0.1},
}


order = 5

panned_results = []

for section, metadata in instruments.items():
  freqz = metadata["freqz"]
  location = metadata["pan"]
  print(f"Filtering {section}... from {freqz[0]} Hz -> {freqz[1]}")
  thistle.filter_wav(*freqz, section, order)
  panned_results.append(thistle.pan_wav(section, location))

print("Done filtering!!!") 
print("Results: ", panned_results)







# PANNING CODE
# filtered_thistle = AudioSegment.from_wav("thistle-filtered.wav")
# filtered_thistle = filtered_thistle.pan(-1)
# filtered_thistle.export("thistle-panned.wav", format="wav")

# instruments = {
#   "dbl_bass": [100.0, 1400.0],
#   "cellos": [65.0, 659.0],
#   "violas": [130.0, 1046.0],
#   "violins": [196.0, 2637.0],
# }


#bandpass double bass 0 hz to 13959 hz
#bandpass celli 40 hz to 9825 hz
#bandpass violas 100 hz to 10000 hz
#bandpass violins 140 hz to 30000 hz