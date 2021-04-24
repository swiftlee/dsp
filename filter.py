from audio import Audio
import matplotlib.pyplot as plt
import numpy as np
import utility
from pathlib import Path
import os
import glob

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def run():
  songs = {
    "A Gift Of Thistle-Gatorchestrators Filter.wav": "thistle.wav",
    "A Knight of the Seven Kingdoms-Gatorchestrators Filter.wav": "kingdoms.wav",
    "Truth-Gatorchestrators Filter.wav": "truth.wav"
  }

  instruments = {
    "dbl_bass": { "freqz": [20.0, 13959.0], "pan": 0.8 },
    "cellos": {"freqz": [40.0, 9825.0], "pan": 0.5},
    "violas": {"freqz": [100.0, 10000.0], "pan": -0.25},
    "violins":{"freqz": [140.0, 20000.0], "pan": -0.8},
  }

  order = 3

  for name, path in songs.items():
    audio_file = Audio(f"./audio/{path}", name)
    print(f"Converting {name} with max volume {audio_file.volume} dB...")
    panned_results = []

    """
    Filtering and panning the song for each frequency range
    """
    for section, metadata in instruments.items():
      freqz = metadata["freqz"]
      location = metadata["pan"]
      # print(f"Filtering {section}... from {freqz[0]} Hz -> {freqz[1]}")
      audio_file.filter_wav(*freqz, section, order)
      panned_results.append(audio_file.pan_wav(section, location))

    """
    Mixing the panned results and writing to a single audio output file
    """
    final = panned_results[0]
    for panned_audio in panned_results[1:]:
      final = final.overlay(panned_audio)

    # Increase volume a bit
    if path == "truth.wav":
      final = final + 4
    else:
      final = final + 2

    Path("./out").mkdir(parents=True, exist_ok=True)
    final.export(f"./out/{name}", format="wav")
    
    print(f"Finished conversion, deleting files...")

    files = glob.glob("./tmp/*", recursive=False)
    for f in files:
      try:
        os.remove(f)
      except OSError as e:
        print(f"Error: {f} : {e.strerror}")


run()