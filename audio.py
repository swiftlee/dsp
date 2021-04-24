from scipy.io import wavfile, loadmat
from scipy.signal import butter, lfilter

class Audio:

  def __init__(self, filepath):
    self.filepath = filepath
    self.fs, self.data = wavfile.read(filepath)
    
  def bandpass(self, min, max, order=5):
    nyq = 0.5 * self.fs
    low = min / nyq
    high = max / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
  

  def bandpass_filter(self, data, min, max, order=5):
    print("Order is: ", order)
    b, a = self.bandpass(min, max, order=order)
    y = lfilter(b, a, data)
    return y

    