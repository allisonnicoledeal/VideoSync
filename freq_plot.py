#  How to track sample rate?
#  Create song class
# http://www.dspguide.com/

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


sample_rate = 44100

# Extract audio from video file, save as wav auido file
# INPUT: Video file
# OUTPUT: Does not return any values, but saves audio as wav file
def extract_audio(video_file):
    track_name = video_file.split(".")
    audio_output = track_name[0] + "WAV.wav"
    audio_data = call(["avconv", "-i", video_file, "-vn", "-f", "wav", audio_output])


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(audio_file):
    rate, data = scipy.io.wavfile.read(audio_file)  # Return the sample rate (in samples/sec) and data from a WAV file
    print "RATE: ", rate
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
    for i in range(int(fft_bin_size - overlap), len(data), fft_bin_size):
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


# Split each second into x samples
# INPUT: list with length of sampling rate
# OUTPUT: list with length of number of indicated samples per second
# def split_samples(mono_data, num_elements_sample):  # num samp sec is 20 if two samples per sec from create samples
#     elements_per_sample = sample_rate/num_elements_sample
#     sample = []
#     for i in range(0, len(mono_data), (elements_per_sample)):
#         added_elements = mono_data[i:i+(elements_per_sample)]
#         sample_avg = sum(added_elements)/len(added_elements)
#         sample.append(sample_avg)

#     return sample


# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
# Reference: http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
def fourier(sample): #, overlap):
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs

    freqs = np.fft.fftfreq(len(sample))  #, overlap) #dont have to recalculate for each sample, pass as parameter

    mag = abs(fft_data) # not necessary
    mag2 = mag**2
    index = np.argmax(mag2)
    freq = freqs[index]  # only valid if index > len(fft_data)/2
    freq_hz = abs(freq*sample_rate)

    return freq_hz


# Plot time vs freq
def plot_d(dict):
    x = []
    y = []

    for item in dict.items():
        for i in range(len(item[1])):
            x.append(item[1][i])
            y.append(item[0])

    plt.plot(x, y, 'ro')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.show()


# Generate list of freq-time tuples
def pairs(d):
    tf_pairs = []

    for item in d.items():
        for i in range(len(item[1])):
            tf_pairs.append((item[0], item[1][i]))

    return sorted(tf_pairs, key=lambda tup:tup[1])


# Compare two value-sorted list objects to see if d1 starts within d2
# INPUT: Two lists, number of consecutive matches to be considered
    # a match, error margin
# OUTPUT: True if match, False if no match
def compare(d1, d2, consec, err):  # start testing err value 10
    i = 0
    j = 0
    time_offset = None
    prev_match = False

    while (i < len(d1)) and (j < len(d2)):
        print "I: ", i
        print "J: ", j
        if j == 0:  # sets the time offset when the first match is found
            time_offset = abs(d1[i][1]-d2[j][1])
            print "J = 0. TIME OFFSET: ", time_offset

        freq_delta = abs(d1[i][0]-d2[j][0])
        print "FREQ DELTA: ", freq_delta
        time_delta = abs(d1[i][1]-d2[j][1])
        print "TIME DELTA: ", time_delta

        if ((freq_delta <= err) and ((time_delta-time_offset) <= 1.0)):  # if potential match (freq err is < given and time offset aligns)
            print "FREQ DELTA ERR SMALL AND TIME OFFSET MATCH"

            time_offset = time_delta
            print 'TIME OFFSET: ', time_offset
            print ""
            i += 1  # go to next index to check if next items match
            j += 1
            prev_match = True
            print "PREV MATCH: ", prev_match

        else:  # reset d2 counter and time offest if match not found
            # print 'MATCH NOT FOUND, INCREASE I, RESET J AND OFFSET'
            if prev_match is False:
                i += 1
     
            j = 0
            time_offset = None
            prev_match = False
            print "PREV MATCH: ", prev_match
            print ""

        if j == consec:
            print consec, "CONSECUTIVE MATCHES FOUND"
            return time_delta

    print consec, 'CONSEC MATCHES NOT FOUND'
    return None


# ===================================================
# FUZZY STRING MATCHING

def letters_dict(dict, dict2):
    letters = {}

    char_index = 65

    for dict_key in dict.keys():
        if dict_key not in letters.keys():
            letters[dict_key] = chr(char_index)
            print 'dict value: ', letters[dict_key]
            char_index += 1

    for dict2_key in dict2.keys():
        if dict2_key not in letters.keys():
            letters[dict2_key] = chr(char_index)
            print 'dict2 value: ', letters[dict2_key]
            char_index += 1

    return letters


def list_from_letters_dict(letters_dict, freq_time_list):
    letter_string = []

    for item in freq_time_list:
            print item
            print item[0]
            print letters_dict
            print letters_dict[item[0]]
            print ""
            letter_string.append(letters_dict[item[0]])

    print letter_string
    return letter_string


# =====================================================
# DTW

def freq_list(freq_time_list):
    freq_array = []
    for item in freq_time_list:
        freq_array.append(item[0])
    return freq_array


# LINEAR REGRESSION
# ---------------------
# from scipy import stats
# x = [5.05, 6.75, 3.21, 2.66]
# y = [1.65, 26.5, -5.93, 7.96]
# gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# print "Gradient and intercept", gradient, intercept
# Gradient and intercept (5.3935773611970186, -16.281127993087829)
# print "R-squared", r_value**2
# R-squared 0.524806275136
# print "p-value", p_value
# p-value 0.27556485788150242




# Test
fftbin = 1024
# Entire file

# sound = extract_audio("HipVsRhy.mp4")
# a1 = read_audio("HipVsRhyWAV.wav")
# a1 = read_audio("Hiphopopotamus.wav")
# a2 = create_samples(a1, 2)
# a3 = process_second(a2, 10)

# Portion of file to compare
soundb = extract_audio("HipClip.mp4")
b0 = read_audio("HipClipWAV.wav")
b1 = b0[44100*10:44100*55]
b2 = process_audio(b1, 1024, 1024*0)
b3 = pairs(b2)
# b4 = sorted(b2.items(), key=lambda x: x[1])
# plot_d(b2)

# soundc = extract_audio("HipVsRhy.mp4")
# c0 = read_audio("HipVsRhyWAV.wav")
c1 = b0[44100*25:44100*40]
c2 = process_audio(c1, 1024, 1024*0)
c3 = pairs(c2)
# plot_d(c2)
# compare(c3, b3, 5, 20)

r5 = freq_list(b3)
s5 = freq_list(c3)

dist, cost, path = mlpy.dtw_std(r5, s5, dist_only=False)
fig = plt.figure(1)
ax = fig.add_subplot(111)
plot1 = plt.imshow(cost.T, origin='lower', cmap=cm.gray, interpolation='nearest')
plot2 = plt.plot(path[0], path[1], 'w')

xlim = ax.set_xlim((-0.5, cost.shape[0]-0.5))
ylim = ax.set_ylim((-0.5, cost.shape[1]-0.5))
plt.show()

# http://glowingpython.blogspot.com/2012/03/linear-regression-with-numpy.html
# http://www2.warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/lin_reg/
def reg_plot(path):
    x = path[1][:]
    y = path[0][:]
    xi = arange(0, len(x))
    gradient, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print "Gradient: ", gradient
    print "intercept: ", intercept

    line = (gradient*xi)+intercept
    plt.plot(x, y, 'ro', xi, (gradient*xi)+intercept, 'r-')
    plt.show()



# r4 = fuzzy_list(r2)
# letters_dictionary = letters_dict(r2, s2)
# r4 = list_from_letters_dict(letters_dictionary, r3)
# s4 = list_from_letters_dict(letters_dictionary, s3)
# print fuzz.partial_ratio(r4, s4)




