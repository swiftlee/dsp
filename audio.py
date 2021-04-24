from scipy.io import wavfile, loadmat
from scipy.signal import butter, lfilter
import utility
import numpy as np
from pydub import AudioSegment

class Audio:

  def __init__(self, filepath, name):
    self.filepath = filepath
    self.fs, self.data = wavfile.read(filepath)
    self.left_channel = self.data[:, 0]
    self.right_channel = self.data[:, 1]
    self.name = name.replace(".wav", "")
    self.volume = AudioSegment.from_wav(filepath).max_dBFS
    
  def bandpass(self, min, max, order=5):
    nyq = 0.5 * self.fs
    low = min / nyq
    high = max / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
  

  def bandpass_filter(self, audio_data, min, max, order=5):
    b, a = self.bandpass(min, max, order=order)
    y = lfilter(b, a, audio_data)
    return y
    
  def write_result(self, filename, audio_data):
    from pathlib import Path
    Path("./tmp").mkdir(parents=True, exist_ok=True)
    wavfile.write(f"./tmp/{filename}", self.fs, audio_data)

  def filter_wav(self, low, high, section, order=5):
    left = self.bandpass_filter(self.left_channel, low, high, order)
    right = self.bandpass_filter(self.right_channel, low, high, order)
    res = [left, right]
    normalized = utility.pcm2float(np.asarray(res).T.astype("int16"), "float32")
    soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")
    filename = f"{self.name}_filtered_{section}.wav"
    self.write_result(filename, utility.float2pcm(soundToPlay.T))
    return filename
  
  def pan_wav(self, section, location):
    audio = AudioSegment.from_wav(f"./tmp/{self.name}_filtered_{section}.wav")
    audio = audio.pan(location)
    # audio.export(f"{self.name}_panned_{section}.wav", format="wav")
    return audio