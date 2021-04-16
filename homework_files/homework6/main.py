import os

from scipy import signal
from scipy.io import wavfile
from scipy.fftpack import fft # fourier transform
import matplotlib.pyplot as plot
import numpy as np


def calc_ITD(sound):
    samplerate, data = wavfile.read("./sounds/" + sound)
    left_channel = data[:, 0]  # get all rows in column 0 (left channel)
    right_channel = data[:, 1]  # get all rows in column 1 (right channel)
    
    left_max = max(left_channel, key=abs)
    right_max = max(right_channel, key=abs)

    time_l = left_channel.tolist().index(left_max)
    time_r = right_channel.tolist().index(right_max)
    
    ITD = (abs(abs(time_l) - abs(time_r)) / samplerate) * 1000
    f = open(f'./ITD/{sound.replace(".wav", ".txt")}', 'w+')
    f.write(f"left_max: {left_max} right_max: {right_max} ITD: {ITD}")
    print(f"left_max: {left_max} right_max: {right_max} ITD: {ITD}, left time: {time_l}, right time: {time_r}")

def create_plots(sound):
    samplerate, data = wavfile.read("./sounds/" + sound)
    left_channel = data[:, 0]  # get all rows in column 0 (left channel)
    right_channel = data[:, 1]  # get all rows in column 1 (right channel)
    normal_left = left_channel / np.linalg.norm(left_channel)
    normal_right = right_channel / np.linalg.norm(right_channel)
  
    time = np.linspace(0, (len(left_channel) / samplerate) * 1000, num=len(left_channel))
    plot.plot(time, left_channel, color="blue")
    plot.plot(time, right_channel, color="red")
    plot.legend(['Left ear', 'Right ear'])
    plot.xlabel("Time (ms)")
    plot.ylabel("Amplitude (normalised)")
    plot.title(sound.replace('.wav', '').capitalize())
    plot.savefig(f'plots/{sound.replace("wav", "png")}')

def create_frequency_plots(sound):
    fs, data = wavfile.read("./sounds/" + sound)
    # fs, Audiodata = wavfile.read(AudioName)

    # Plot the audio signal in time
    plot.plot(data[:, 1])
    plot.title('Audio signal in time',size=16)

    # spectrum
    n = len(data[:, 1]) 
    AudioFreq = fft(data[:, 1])
    AudioFreq = AudioFreq[0:int(np.ceil((n+1)/2.0))] #Half of the spectrum
    MagFreq = np.abs(AudioFreq) # Magnitude
    MagFreq = MagFreq / float(n)
    # power spectrum
    MagFreq = MagFreq**2
    if n % 2 > 0: # ffte odd 
        MagFreq[1:len(MagFreq)] = MagFreq[1:len(MagFreq)] * 2
    else:# fft even
        MagFreq[1:len(MagFreq) -1] = MagFreq[1:len(MagFreq) - 1] * 2 

    plot.figure()
    freqAxis = np.arange(0,int(np.ceil((n+1)/2.0)), 1.0) * (fs / n);
    plot.plot(freqAxis/1000.0, 10*np.log10(MagFreq)) #Power spectrum
    plot.xlabel('Frequency (kHz)'); plot.ylabel('Power spectrum (dB)');

    #Spectrogram
    N = 512 #Number of point in the fft
    f, t, Sxx = signal.spectrogram(data[:, 1], fs,window = signal.blackman(N),nfft=N)
    plot.figure()
    plot.pcolormesh(t, f,10*np.log10(Sxx)) # dB spectrogram
    #plot.pcolormesh(t, f,Sxx) # Lineal spectrogram
    plot.ylabel('Frequency [Hz]')
    plot.xlabel('Time [seg]')
    plot.title('Spectrogram with scipy.signal',size=16);

    plot.savefig(f'./plots/{sound.replace(".wav", "-spectrogram.png")}')
    # plot.show()

def create_periodogram(sound):
    fs, data = wavfile.read("./sounds/" + sound)
    left_channel = data[:, 1]
    # Fixing random state for reproducibility
    # np.random.seed(19680801)

    dt = 0.00005
    t = np.arange(0, 10, dt)
    r = np.exp(-t / 0.05)

    cnse = np.convolve(left_channel, r) * dt
    cnse = cnse[:len(t)]
    s = 0.1 * np.sin(2 * np.pi * t) + cnse

    # plot.subplot(211)
    # plot.plot(t, s)
    # plot.subplot(212)
    plot.psd(s, 512, 1 / dt)

    #time = (0:1)/(fs:len(left_channel))
    #pxx = psd(spectrum.periodogram, left_channel, 'Fs', fs, 'NFFT', len(left_channel))
    #plot.savefig(f'./plots/{sound.replace(".wav", "-periodogram.png")}')
    # plot.psd(left_channel, Fs=fs, NFFT=len(left_channel))
    plot.savefig(f'./plots/{sound.replace(".wav", "-periodogram-right.png")}')
    plot.clf()


for file in os.listdir("./sounds"):
    # create_plots(file)
    # create_frequency_plots(file)
    # create_periodogram(file)
    calc_ITD(file)
