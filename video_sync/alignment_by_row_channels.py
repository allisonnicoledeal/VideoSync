from __future__ import absolute_import, division, print_function, unicode_literals

import math
from collections import defaultdict
from subprocess import call

import numpy as np
import scipy.io.wavfile
from scipy import signal


# Extract audio from video file, save as wav audio file
# INPUT: Video file
# OUTPUT: Does not return any values, but saves audio as wav file
def extract_audio(dir_, video_file):
    track_name = video_file.split(".")
    audio_output = track_name[0] + "WAV.wav"  # !! CHECK TO SEE IF FILE IS IN UPLOADS DIRECTORY
    output = dir_ + audio_output
    call(["ffmpeg", "-y", "-i", dir_ + video_file, "-vn", "-ac", "1", "-f", "wav", output])
    return output


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(audio_file):
    rate, data = scipy.io.wavfile.read(audio_file)  # Return the sample rate (in samples/sec) and data from a WAV file
    return data, rate


def make_horiz_bins(data, fft_bin_size, overlap, box_height):
    horiz_bins = defaultdict(list)
    # process first sample and set matrix height
    sample_data = data[0:fft_bin_size]  # get data for first sample
    if len(sample_data) == fft_bin_size:  # if there are enough audio points left to create a full fft bin
        intensities = fourier(sample_data)  # intensities is list of fft results
        for i, intensity in enumerate(intensities):
            box_y = i // box_height
            horiz_bins[box_y].append((intensity, 0, i))  # (intensity, x, y)
    # process remainder of samples
    x_coord_counter = 1  # starting at second sample, with x index 1
    for i in range(int(fft_bin_size - overlap), len(data), int(fft_bin_size - overlap)):
        sample_data = data[i:i + fft_bin_size]
        if len(sample_data) == fft_bin_size:
            intensities = fourier(sample_data)
            for j, intensity in enumerate(intensities):
                box_y = j // box_height
                horiz_bins[box_y].append((intensity, x_coord_counter, j))  # (intensity, x, y)
        x_coord_counter += 1

    return horiz_bins


# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
def fourier(sample):  # , overlap):
    mag = []
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs
    for i in range(len(fft_data) // 2):
        r = fft_data[i].real ** 2
        j = fft_data[i].imag ** 2
        mag.append(round(math.sqrt(r + j), 2))

    return mag


def make_vert_bins(horiz_bins, box_width):
    boxes = defaultdict(list)
    for key in horiz_bins:
        for bin_ in horiz_bins[key]:
            box_x = bin_[1] // box_width
            boxes[(box_x, key)].append(bin_)
    return boxes


def find_bin_max(boxes, maxes_per_box):
    freqs_dict = defaultdict(list)
    for key in boxes:
        max_intensities = [(1, 2, 3)]
        for box in boxes[key]:
            if box[0] > min(max_intensities)[0]:
                if len(max_intensities) < maxes_per_box:  # add if < number of points per box
                    max_intensities.append(box)
                else:  # else add new number and remove min
                    max_intensities.append(box)
                    max_intensities.remove(min(max_intensities))
        for max_intensity in max_intensities:
            freqs_dict[max_intensity[2]].append(max_intensity[1])
    return freqs_dict


def find_freq_pairs(freqs_dict_orig, freqs_dict_sample):
    return [(t1, t2)
            for key in freqs_dict_sample
            if key in freqs_dict_orig
            for t1 in freqs_dict_sample[key]
            for t2 in freqs_dict_orig[key]]


def find_delay(time_pairs):
    t_diffs = defaultdict(int)
    for t1, t2 in time_pairs:
        t_diffs[t1 - t2] += 1
    t_diffs_sorted = sorted(t_diffs.items(), key=lambda x: x[1])
    print(t_diffs_sorted)
    time_delay = t_diffs_sorted[-1][0]

    return time_delay


# Find time delay between two video files
def align(video1, video2, dir_, fft_bin_size=1024, overlap=0, box_height=512, box_width=43, samples_per_box=7):
    # Process first file
    wav_file1 = extract_audio(dir_, video1)
    raw_audio1, rate1 = read_audio(wav_file1)

    bins_dict1 = make_horiz_bins(raw_audio1, fft_bin_size, overlap,
                                 box_height)  # bins, overlap, box height
    boxes1 = make_vert_bins(bins_dict1, box_width)  # box width
    ft_dict1 = find_bin_max(boxes1, samples_per_box)  # samples per box

    # Process second file
    wav_file2 = extract_audio(dir_, video2)
    raw_audio2, rate2 = read_audio(wav_file2)

    if rate1 == rate2:
        rate = rate1
    else:  # resampling
        secs = len(raw_audio2) // rate2
        new_sample_count = secs * rate1
        raw_audio2 = signal.resample(raw_audio2, new_sample_count)

        rate = rate1

    bins_dict2 = make_horiz_bins(raw_audio2, fft_bin_size, overlap, box_height)
    boxes2 = make_vert_bins(bins_dict2, box_width)
    ft_dict2 = find_bin_max(boxes2, samples_per_box)

    # Determine time delay
    pairs = find_freq_pairs(ft_dict1, ft_dict2)
    delay = find_delay(pairs)
    samples_per_sec = rate / fft_bin_size
    seconds = round(delay / samples_per_sec, 4)

    if seconds > 0:
        return seconds, 0
    else:
        return 0, abs(seconds)

# ======= TEST FILES ==============
# audio1 = "regina6POgShQ-lC4.mp4"
# # audio2 = "reginaJo2cUWpILMgWAV.wav"
# audio1 = "Settle2kFaZIKtcn6s.mp4"
# audio2 = "Settle2d_tj-9_dGog.mp4"
# audio1 = "DanielZ5PPlk53IMY.mp4"
# audio2 = "Daniel08ycq2T_ab4.mp4"
# directory = "./uploads/"
# t = align(audio1, audio2, directory)
# print(t)
