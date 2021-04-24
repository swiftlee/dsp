from audio import Audio
import matplotlib.pyplot as plt
from scipy.signal import freqz
import numpy as np

# T = 0.05
# nsamples = int(T * 5000.0)
# t = np.linspace(0, T, nsamples, endpoint=False)
# a = 0.02
# f0 = 600.0
# x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
# x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
# x += a * np.cos(2 * np.pi * f0 * t + .11)
# x += 0.03 * np.cos(2 * np.pi * 2000 * t)
# plt.figure(2)
# plt.clf()
# plt.plot(t, x, label='Noisy signal')
# plt.savefig('test.png')

thistle = Audio("thistle.wav")
xmax = 30
xmin = 29.95
low_stop = 500.0
high_stop = 1250.0
order = 5

numsamples = int((xmax-xmin) * thistle.fs)
t = np.linspace(xmin, xmax, numsamples, endpoint=False)
xvalues = thistle.data[:, 0][300000:(300000 + numsamples)]
plt.plot(t, xvalues, label="Unfiltered signal")
y = thistle.bandpass_filter(xvalues, low_stop, high_stop, 5)
plt.plot(t, y, label='Filtered signal')
plt.xlabel('time (seconds)')
plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')
plt.savefig("signal.png")