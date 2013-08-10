#  How to track sample rate?
#  Create song class
# http://www.dspguide.com/

# generate thumbnails: ffmpeg -i input.flv -an -ss 1:00:00 -r 1 -vframes 1 -f mjpeg -y output.jpg

import scipy.io.wavfile
from scipy import stats
import numpy as np
from numpy import arange
from subprocess import call
import math
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import mlpy
import dtw

sample_rate = 44100

# Extract audio from video file, save as wav auido file
# INPUT: Video file
# OUTPUT: Does not return any values, but saves audio as wav file
def extract_audio(dir, video_file):
    track_name = video_file.split(".")
    audio_output = track_name[0] + "WAV.wav"
    output = dir + audio_output
    audio_data = call(["avconv", "-i", dir+video_file, "-vn", "-f", "wav", output])
    # audio_data = call(["avconv", "-n", "-i", dir+video_file, "-vn", "-f", "wav", output])
    return output


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(audio_file):
    rate, data = scipy.io.wavfile.read(audio_file)  # Return the sample rate (in samples/sec) and data from a WAV file
    # print "RATE: ", rate
    return data


# sample span: length of sample (44100 is one second)
# overlap: number of data elements overlapping between samples
def process_audio(data, fft_bin_size, overlap):
    d = {}

    # process first sample
    sample_data = data[0:fft_bin_size]
    if (len(sample_data) == fft_bin_size):
        freq_max = process_sample(sample_data)
        dict_key = round(freq_max, 2)
        second = float((float(fft_bin_size)/2.0)/float(sample_rate))
        dict_value = round(second, 3)

        if dict_key in d.keys() is not None:   # if dict key exists, append
            d[dict_key].append(dict_value)  # dict_key is max freq and dict_value is time
        else:  # else create dict key and assign value
            d[dict_key] = [dict_value]

    # process remainder of samples
    for i in range(int(fft_bin_size - overlap), len(data), int(fft_bin_size-overlap)):
        sample_data = data[i:i + fft_bin_size]
        if (len(sample_data) == fft_bin_size):
            freq_max = process_sample(sample_data)
            dict_key = round(freq_max, 2)
            second = float((float(i) + float(fft_bin_size)/2.0)/float(sample_rate))
            dict_value = round(second, 3)

            if dict_key in d.keys() is not None:   # if dict key exists, append
                d[dict_key].append(dict_value)  # dict_key is max freq and dict_value is time
            else:  # else create dict key and assign value
                d[dict_key] = [dict_value]

    return d


# process individual sample
def process_sample(data):
        avg = channel_avg(data)
        # print 'LEN AVG, SHOULD BE 1024', len(avg)
        freq = fourier(avg)
        # print 'freq: ', freq

        return freq

# =================================================================

# Average Left and right audio channels
# INPUT: M x 2 matrix, list of 2-element lists (L and R channels)
# OUTPUT: M x 1 matrix, list
def channel_avg(raw_data_matrix):
    data_channel_avg = []
    for i in range(len(raw_data_matrix)):
        average = (raw_data_matrix[i][0] + raw_data_matrix[i][1]) / 2
        data_channel_avg.append(average)

    return data_channel_avg



# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
# Reference: http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
def fourier(sample):  #, overlap):
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs

    freqs = np.fft.fftfreq(len(sample))  #, overlap) #dont have to recalculate for each sample, pass as parameter

    mag = abs(fft_data) # not necessary
    mag2 = mag**2
    index = np.argmax(mag2)
    freq = freqs[index]  # only valid if index > len(fft_data)/2
    freq_hz = abs(freq*sample_rate)

    return freq_hz


# Generate list of freq-time tuples
def pairs(d):
    tf_pairs = []

    for item in d.items():
        for i in range(len(item[1])):
            tf_pairs.append((item[0], item[1][i]))

    return sorted(tf_pairs, key=lambda tup:tup[1])


# DTW

def freq_list(freq_time_list):
    freq_array = []
    for item in freq_time_list:
        freq_array.append(item[0])
    return freq_array


def find_start(base_freqs, sample_freqs, consec, err):
    sample_start = sum(sample_freqs[:consec])
    potential_start_indices = []

    for i in range(len(base_freqs)):
        base_start = sum(base_freqs[i:i+consec])
        if (base_start < sample_start+err) and (base_start > sample_start-err):
            potential_start_indices.append(i)

    return potential_start_indices


def best_start(base_freqs, sample_freqs, potential_start_indices):
    distances = float("inf")
    start_index = None
    for i in range(len(potential_start_indices)):
        start_point = potential_start_indices[i]
        dist, cost, path = mlpy.dtw_std(base_freqs[start_point:start_point+len(sample_freqs)], sample_freqs, dist_only=False)

        if dist < distances:
            print potential_start_indices[i]
            print dist
            print ""
            distances = dist
            start_index = start_point

    return start_index


# def analyze(video1_base, video2_sample, dir):
#     sound_base = extract_audio(dir, video1_base)
#     base0 = read_audio(sound_base)
#     base1 = base0[44100*12:44100*50]
#     base2 = process_audio(base1, 1024, 1024*.25)
#     base3 = pairs(base2)
#     base5 = freq_list(base3)

#     sound_sample = extract_audio(dir, video2_sample)
#     sample0 = read_audio(sound_sample)
#     sample1 = sample0[44100*12:44100*30]
#     sample2 = process_audio(sample1, 1024, 1024*.25)
#     sample3 = pairs(sample2)
#     sample5 = freq_list(sample3)

#     start_points = find_start(base5, sample5, 6, 50)
#     print "start points:", start_points
#     alignment = best_start(base5, sample5, start_points)
#     print "alignment: ", alignment
#     secs = base3[alignment][1]  # must be longer sample
#     print "sec: ", secs

#     return (0, secs)  # returns tuple of long video delay, short video delay


#========== TESTING============
# dir = "./uploads/"
# # video1_base = "Gold.mp4"
# # video2_sample = "HipClip.mp4"
# # video1_base = "regina6POgShQ-lC4.mp4"
# # video2_sample = "reginaJo2cUWpILMg.mp4"
# # video1_base = "regina6POgShQ-lC4.mp4"
# # video2_sample = "reginaJo2cUWpILMg.mp4"
# video1_base = "Gold.mp4"
# video2_sample = "Gold.mp4"
# # video2_sample = "Reg2.mp4"

# sound_base = extract_audio(dir, video1_base)
# base0 = read_audio(sound_base)
# base1 = base0[44100*0:44100*50]
# base2 = process_audio(base1, 1024, 1024*.25)
# base3 = pairs(base2)
# base5 = freq_list(base3)

# sound_sample = extract_audio(dir, video2_sample)
# sample0 = read_audio(sound_sample)
# sample1 = sample0[44100*11:44100*30]
# sample2 = process_audio(sample1, 1024, 1024*.25)
# sample3 = pairs(sample2)
# sample5 = freq_list(sample3)

# start_points = find_start(base5, sample5, 6, 50) # 6, 50 has been working
# print "start points:", start_points
# alignment = best_start(base5, sample5, start_points)
# print "alignment: ", alignment
# secs = base3[alignment][1]  # must be longer sample
# print "sec: ", secs




#========== TEST ================
# offset = analyze("regina6POgShQ-lC4.mp4", "reginaJo2cUWpILMg.mp4", "./uploads/")
# offset = analyze("Reg1.mp4", "Reg2.mp4")
# offset = analyze("HipVsRhy.mp4", "HipClip.mp4")

# http://www.youtube.com/watch?v=6POgShQ-lC4
# http://www.youtube.com/watch?v=Jo2cUWpILMg
# http://www.youtube.com/watch?v=FKbWPHRCJm8
# http://www.youtube.com/watch?v=R49i0BzIiHc




# =========== FREQUENCY COMPARISON ============
# Compare two value-sorted list objects to see if d1 starts within d2
# INPUT: Two lists, number of consecutive matches to be considered
    # a match, error margin
# OUTPUT: True if match, False if no match
# def compare(d1, d2, consec, err):  # start testing err value 10
#     i = 0
#     j = 0
#     time_offset = None
#     prev_match = False

#     while (i < len(d1)) and (j < len(d2)):
#         print "I: ", i
#         print "J: ", j
#         if j == 0:  # sets the time offset when the first match is found
#             time_offset = abs(d1[i][1]-d2[j][1])
#             print "J = 0. TIME OFFSET: ", time_offset

#         freq_delta = abs(d1[i][0]-d2[j][0])
#         print "FREQ DELTA: ", freq_delta
#         time_delta = abs(d1[i][1]-d2[j][1])
#         print "TIME DELTA: ", time_delta

#         if ((freq_delta <= err) and ((time_delta-time_offset) <= 1.0)):  # if potential match (freq err is < given and time offset aligns)
#             print "FREQ DELTA ERR SMALL AND TIME OFFSET MATCH"

#             time_offset = time_delta
#             print 'TIME OFFSET: ', time_offset
#             print ""
#             i += 1  # go to next index to check if next items match
#             j += 1
#             prev_match = True
#             print "PREV MATCH: ", prev_match

#         else:  # reset d2 counter and time offest if match not found
#             # print 'MATCH NOT FOUND, INCREASE I, RESET J AND OFFSET'
#             if prev_match is False:
#                 i += 1
     
#             j = 0
#             time_offset = None
#             prev_match = False
#             print "PREV MATCH: ", prev_match
#             print ""

#         if j == consec:
#             print consec, "CONSECUTIVE MATCHES FOUND"
#             return time_delta

#     print consec, 'CONSEC MATCHES NOT FOUND'
#     return None



# ========== TIME VS. FREQ PLOT ============
# Plot time vs freq
# def plot_d(dict):
#     x = []
#     y = []

#     for item in dict.items():
#         for i in range(len(item[1])):
#             x.append(item[1][i])
#             y.append(item[0])

#     plt.plot(x, y, 'ro')
#     plt.xlabel('Time')
#     plt.ylabel('Frequency')
#     plt.show()



# ===================================================
# # FUZZY STRING MATCHING

# def letters_dict(dict, dict2):
#     letters = {}

#     char_index = 65

#     for dict_key in dict.keys():
#         if dict_key not in letters.keys():
#             letters[dict_key] = chr(char_index)
#             print 'dict value: ', letters[dict_key]
#             char_index += 1

#     for dict2_key in dict2.keys():
#         if dict2_key not in letters.keys():
#             letters[dict2_key] = chr(char_index)
#             print 'dict2 value: ', letters[dict2_key]
#             char_index += 1

#     return letters


# def list_from_letters_dict(letters_dict, freq_time_list):
#     letter_string = []

#     for item in freq_time_list:
#             print item
#             print item[0]
#             print letters_dict
#             print letters_dict[item[0]]
#             print ""
#             letter_string.append(letters_dict[item[0]])

#     print letter_string
#     return letter_string



