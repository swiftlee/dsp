from scipy import signal
from scipy.io import wavfile, loadmat
import matplotlib.pyplot as plt
import numpy as np
import utility

# declare variables
result_left = []
result_right = []
increment = 1
current_sample_index = 0
aIndex = 0
eIndex = 9
azimuths = np.array([-80, -65, -55, *range(-45, 50, 5), 55, 65, 80])
elevations = -45
for x in range(0, 49):  # elevations = -45 + 5.625 * range(0, 49)
    elevations += 5.625 * x

np.set_printoptions(precision=6)

"""Read in the song file, 'data' will be a 2D array with one column for each channel"""
samplerate, data = wavfile.read("thistle.wav")
# print(data)
# data = utility.pcm2float(np.asarray(data).astype("int16"), "float32")
# print(data)
# rows = len(data)
# columns = len(data[0])
# print(f"rows: {rows} columns: {columns}")

"""Set the left/right channel and frame size variables"""
left_channel = data[:, 0]  # get all rows in column 0 (left channel)
right_channel = data[:, 1]  # get all rows in column 1 (right channel)
frame_size = int(np.ceil(samplerate / 2))

"""Load in and initialize the relevant variables from the HRTF"""
hrtf = loadmat("CIPIC_58_HRTF.mat")
hrir_r = hrtf["hrir_r"]
hrir_l = hrtf["hrir_l"]
ITD = hrtf["ITD"]  # 2D array with many columns/rows

# more debugging
# s = (2400, 2)
# buffer = np.zeros(s)

"""Iterate until our current index exceeds the data length"""
while current_sample_index < len(data):
    # debugging stuff
    # current_sample_index = int(np.ceil(len(data) / 2))
    # frame_size = 100
    # left_channel = left_channel[current_sample_index:]

    """If on the next iteration current_sample_index will exceed len(data)
    we must adjust the frame size to ensure we convolve the end of the song file"""
    if (current_sample_index + frame_size) > len(data):
        frame_size = len(data) - current_sample_index

    """Clear wav_left and wav_right arrays"""
    wav_left = []
    wav_right = []

    """Set the azimuth index"""
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

    # np.savetxt("before_conv.txt", wav_left)

    wav_left = np.asarray(signal.convolve(wav_left, lft, mode="same"))
    # np.savetxt("after_conv.txt", wav_left)
    # break
    wav_right = np.asarray(signal.convolve(wav_right, rgt, mode="same"))

    if aIndex < 12:
        wav_left = np.append(wav_left, np.zeros(abs(delay)))
        wav_right = np.append(np.zeros(abs(delay)), wav_right)
    else:
        wav_left = np.append(np.zeros(abs(delay)), wav_left)
        wav_right = np.append(wav_right, np.zeros(abs(delay)))

    # debug, remove later
    # result_left = np.append(result_left, buffer)
    # result_right = np.append(result_right, buffer)
    # print(f"result_left: {result_left}")
    # print(f"wav_left: {wav_left}")
    result_left = np.append(result_left, wav_left)
    # print(f"result length: {len(result_left)}")

    result_right = np.append(result_right, wav_right)

    left_channel = left_channel[frame_size:]
    # print(f"left_channel length: {len(left_channel)}")

    right_channel = right_channel[frame_size:]
    current_sample_index += frame_size

    # if current_sample_index == (frame_size * 6):
    #     result_left = np.append(result_left[(frame_size * 4) :], wav_left)
    #     result_right = np.append(result_right[(frame_size * 4) :], wav_right)
    #     print("breaking out")
    #     break

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


# Before further processing, we normally want to convert the signals to floating point values
# and normalize them to a range from -1 to 1 by dividing all values by the largest possible value.
normalized = utility.pcm2float(np.asarray(convolved_data).T.astype("int16"), "float32")
soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")

wavfile.write("scipy_float32.wav", samplerate, soundToPlay.T)
wavfile.write("scipy_pcm16.wav", samplerate, utility.float2pcm(soundToPlay.T, "int16"))

# # https://docs.scipy.org/doc/scipy/reference/signal.html


# write all to individual files
# go back over and concat them
# make sure it comes out to same file size
