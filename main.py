from scipy import signal
from scipy.io import wavfile, loadmat
import matplotlib.pyplot as plt
import numpy as np
import utility

azimuths = np.array([-80, -65, -55, *range(-45, 50, 5), 55, 65, 80])

# elevations = -45 + 5.625 * range(0, 49)
elevations = -45
for x in range(0, 49):
    elevations += 5.625 * x
# print(azimuths)
# print(elevations)
aIndex = 0
eIndex = 9

np.set_printoptions(precision=6)

samplerate, data = wavfile.read("thistle.wav")
print(samplerate)
hrtf = loadmat("CIPIC_58_HRTF.mat")
hrir_r = hrtf["hrir_r"]
hrir_l = hrtf["hrir_l"]

# for i in range(1, len(hrir_l)):
#     print(f"Index: {i} entry: {hrir_l[i]}")

ITD = hrtf["ITD"]

left_channel = data[:, 0]
right_channel = data[:, 1]
result_left = []
result_right = []
increment = 1
current_sample_index = 0
frame_size = int(np.ceil(samplerate / 2))
print(frame_size)
while current_sample_index < len(data):
    if (current_sample_index + frame_size) > len(data):
        frame_size = len(data) - current_sample_index
    wav_left = []
    wav_right = []
    aIndex = aIndex + increment
    if aIndex == 0:
        eIndex = 8

    if aIndex == 24:
        increment = -1
        eIndex = 48
    elif aIndex == 1:
        increment = 1
        eIndex = 8

    lft = np.squeeze(hrir_l[aIndex, eIndex, :])
    rgt = np.squeeze(hrir_r[aIndex, eIndex, :])
    delay = int(ITD[aIndex, eIndex])
    # print(f"left: {lft}")

    # print(f"THE DELAY IS: {delay}")

    wav_left = left_channel[:frame_size]
    wav_right = right_channel[:frame_size]
    # print(f"Wav_left length: {len(wav_left)}")
    wav_left = np.asarray(signal.convolve(wav_left, lft, mode="same"))
    print(f"wav_left {len(wav_left)}")
    wav_right = np.asarray(signal.convolve(wav_right, rgt, mode="same"))

    if aIndex < 12:
        wav_left = np.append(wav_left, np.zeros(abs(delay)))
        wav_right = np.append(np.zeros(abs(delay)), wav_right)
    else:
        wav_left = np.append(np.zeros(abs(delay)), wav_left)
        wav_right = np.append(wav_right, np.zeros(abs(delay)))

    result_left = np.append(result_left, wav_left)
    # print(f"result length: {len(result_left)}")

    result_right = np.append(result_right, wav_right)

    left_channel = left_channel[(frame_size + 10) :]
    # print(f"left_channel length: {len(left_channel)}")

    right_channel = right_channel[(frame_size + 10) :]
    current_sample_index += frame_size

# a[start:stop]  # items start through stop-1
# a[start:]      # items start through the rest of the array
# a[:stop]       # items from the beginning through stop-1
# a[:]           # a copy of the whole array

# if (aIndex < 13) %sound is on left so delay right
#     wav_left = [wav_left zeros(size(1:abs(delay)))];
#     wav_right =[zeros(size(1:abs(delay))) wav_right];
# else
#     wav_left = [zeros(size(1:abs(delay))) wav_left];
#     wav_right =[wav_right zeros(size(1:abs(delay)))];
# end
# END OF WHILE LOOP


# left_channel = np.asarray(signal.convolve(lft, left_channel))
# right_channel = np.asarray(signal.convolve(rgt, right_channel))
print(f"length left: {len(result_left)}")
print(f"length right: {len(result_right)}")
print(f"current_sample_index: {current_sample_index}")
print(f"frame_size: {frame_size}")
convolved_data = [0, 0]
convolved_data[0] = result_left
convolved_data[1] = result_right
# print(f"length of {len(np.asarray(convolved_data).T)} {np.asarray(convolved_data)}")
# print(f"but data length is: {len(np.asarray(data))}")
# print(lft)
# print("---------------------------")
# print(rgt)
# delay = hrtfStruct.ITD(aIndex, eIndex);
# wav_left = [wav_left conv(lft, sig(:,1)')];
# wav_right = [wav_right conv(rgt, sig(:,2)')];

# np.asarray(convolved_data).astype("int16")

# Before further processing, we normally want to convert the signals to floating point values
# and normalize them to a range from -1 to 1 by dividing all values by the largest possible value.
normalized = utility.pcm2float(np.asarray(convolved_data).T.astype("int16"), "float32")
# print(normalized)
soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")

wavfile.write("scipy_float32.wav", samplerate, soundToPlay.T)
wavfile.write("scipy_pcm16.wav", samplerate, utility.float2pcm(soundToPlay.T, "int16"))

# https://docs.scipy.org/doc/scipy/reference/signal.html
# np.convolve ?
# scipy.signal.convolve ?
# lft = np.squeeze()
