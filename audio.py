from scipy.io import wavfile, loadmat
from scipy.signal import butter, lfilter

class Audio:

  def __init__(self, filepath):
    self.filepath = filepath
    self.fs, self.data = wavfile.read(filepath)
    self.left_channel = self.data[:, 0]
    self.right_channel = self.data[:, 1]
    
  def bandpass(self, min, max, order=5):
    nyq = 0.5 * self.fs
    low = min / nyq
    high = max / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
  

  def bandpass_filter(self, audio_data, min, max, order=5):
    b, a = self.bandpass(min, max, order=order)
    y = lfilter(b, a, audio_data)
    print(len(y))
    return y
    
  def write_result(self, filename, audio_data):
    wavfile.write(filename, self.fs, audio_data)