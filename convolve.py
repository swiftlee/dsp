# write all to individual files
# go back over and concat them
# make sure it comes out to same file size
import os
from scipy import signal
from scipy.io import wavfile, loadmat
import matplotlib.pyplot as plt
import numpy as np
import utility
from pydub import AudioSegment as aus


"""If on the next iteration current_sample_index will exceed len(data)
we must adjust the frame size to ensure we convolve the end of the song file"""


def calc_frame_size(current_sample_index, frame_size, data_length):
    if (current_sample_index + frame_size) > data_length:
        frame_size = data_length - current_sample_index
    return frame_size


"""Set the azimuth index"""


def calc_elevation(aIndex):
    if aIndex == 24:
        return 48
    return 8


def calc_increment(aIndex):
    if aIndex == 24:
        return -1
    return 1


def create_combined_file():
    # TODO read in each file in the tmp directory and concat onto an audio segment file
    dir = "./tmp/"
    filelist = os.listdir(dir)
    combined = aus.empty()
    for filename in sorted(filelist):
        filename = dir + filename
        segment = aus.from_wav(filename)
        combined = combined + segment
        # print(filename)

    combined.export("combined.wav", format="wav")


def write_pieces(data, samplerate):
    for row in range(len(data)):
        left = data[row][0]
        right = data[row][1]
        convolved_data = [0, 0]
        convolved_data[0] = left
        convolved_data[1] = right
        normalized = utility.pcm2float(
            np.asarray(convolved_data).T.astype("int16"), "float32"
        )
        soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")
        filename = f"./tmp/0{row}piece.wav" if row < 10 else f"./tmp/{row}piece.wav"
        wavfile.write(filename, samplerate, soundToPlay.T)


def write_to_file(left, right, samplerate):
    convolved_data = [0, 0]
    convolved_data[0] = left
    convolved_data[1] = right

    """Before further processing, we normally want to convert the signals to floating point values and normalize them to a range from -1 to 1 by dividing all values by the largest possible value."""
    normalized = utility.pcm2float(
        np.asarray(convolved_data).T.astype("int16"), "float32"
    )
    soundToPlay = np.array([normalized[:, 0], normalized[:, 1]], dtype="float32")

    wavfile.write("result32.wav", samplerate, soundToPlay.T)
    wavfile.write("result16.wav", samplerate, utility.float2pcm(soundToPlay.T, "int16"))


def convert_audio(file):
    # declare variables
    convolved = []
    result_left = []
    result_right = []
    increment = 1
    current_sample_index = 0
    aIndex = 0
    eIndex = 8
    azimuths = np.array([-80, -65, -55, *range(-45, 50, 5), 55, 65, 80])
    elevations = -45
    for x in range(0, 49):  # elevations = -45 + 5.625 * range(0, 49)
        elevations += 5.625 * x

    np.set_printoptions(precision=6)

    samplerate, data = wavfile.read(file)

    """Set the left/right channel and frame size variables"""
    left_channel = data[:, 0]  # get all rows in column 0 (left channel)
    right_channel = data[:, 1]  # get all rows in column 1 (right channel)
    frame_size = int(np.ceil(samplerate / 2))

    """Load in and initialize the relevant variables from the HRTF"""
    hrtf = loadmat("CIPIC_58_HRTF.mat")
    hrir_r = hrtf["hrir_r"]
    hrir_l = hrtf["hrir_l"]
    ITD = hrtf["ITD"]  # 2D array with many columns/rows

    print("Convolving...")
    done = False
    while current_sample_index < len(data):
        """If on the next iteration current_sample_index will exceed len(data)
        we must adjust the frame size to ensure we convolve the end of the song file"""
        if (current_sample_index + frame_size) > len(data):
            frame_size = len(data) - current_sample_index

        aIndex += increment
        frame_size = calc_frame_size(current_sample_index, frame_size, len(data))
        eIndex = calc_elevation(aIndex)
        increment = calc_increment(aIndex)

        """Clear wav and convolved arrays"""
        wav_left = []
        wav_right = []
        convolved_left = []
        convolved_right = []

        """Get left/right squeeze values and delay"""
        lft = np.squeeze(hrir_l[aIndex, eIndex, :])
        rgt = np.squeeze(hrir_r[aIndex, eIndex, :])
        delay = int(ITD[aIndex, eIndex])

        """Put left and right channel segments into temporary wav variables"""
        wav_left = left_channel[:frame_size]
        wav_right = right_channel[:frame_size]

        """Perform the convolutions"""
        # convolved_left = np.asarray(signal.convolve(wav_left, lft, mode="same"))
        # convolved_right = np.asarray(signal.convolve(wav_right, rgt, mode="same"))
        convolved_left = np.asarray(signal.convolve(lft, wav_left))
        convolved_right = np.asarray(signal.convolve(rgt, wav_right))

        """Correcting for specific ear delays"""
        if aIndex < 12:
            convolved_left = np.append(convolved_left, np.zeros(abs(delay)))
            convolved_right = np.append(np.zeros(abs(delay)), convolved_right)
        else:
            convolved_left = np.append(np.zeros(abs(delay)), convolved_left)
            convolved_right = np.append(convolved_right, np.zeros(abs(delay)))

        """Append convolved to results"""
        # result_left = np.append(result_left, convolved_left)
        # result_right = np.append(result_right, convolved_right)

        """Instead of appending the data, append the arrays and write to files later"""
        convolved.append([convolved_left, convolved_right])

        """Increment left/right channels and index"""
        left_channel = left_channel[frame_size:]
        right_channel = right_channel[frame_size:]
        current_sample_index += frame_size
    """END OF WHILE LOOP"""

    print("Writing to file...")
    write_pieces(convolved, samplerate)
    # write_to_file(result_left, result_right, samplerate)
    print("Finished writing")

    create_combined_file()


thistle = "thistle.wav"
omt = "OMT.wav"
convert_audio(thistle)