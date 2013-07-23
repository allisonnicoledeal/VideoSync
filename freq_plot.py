#  How to track sample rate?
#  Create song class

import scipy.io.wavfile
import numpy as np


sample_rate = 44100

# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(file):
    rate, data = scipy.io.wavfile.read(file)  # Return the sample rate (in samples/sec) and data from a WAV file
    sample_rate = rate
    return data


def create_samples(data):
    s = {}
    second = 0
    for i in range(0, len(data), sample_rate):
        s[second] = data[i:i+sample_rate]
        second+=1

    return s


# Process samples by second
# INPUT: Dictionary of seconds as keys and matrix of L R raw audio data as values
# OUTPUT: Returns dictionary of key(frequency) value(time) pairs
def process_second(s, num):
    d = {}
    for i in range(len(s)):  # for second in song
        mono = channel_avg(s[i])
        split = split_samples(mono, num)
        fft = fourier(split)
        max = max_freq(fft, i)

        if max[0] in d.keys() is not None:   # if dict key exists, append
            d[max[0]].append(max[1])  # dict_key is max freq and dict_value is time
        else:  # else create dict key and assign value
            d[max[0]] = max[1]
 
    return d


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
def split_samples(mono_data, num_samp_sec):
    elements_per_sample = sample_rate/num_samp_sec
    sample = []
    for i in range(0, len(mono_data), (elements_per_sample)):
        added_elements = mono_data[i:i+(elements_per_sample)]
        sample_avg = sum(added_elements)/len(added_elements)
        sample.append(sample_avg)

    return sample


# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
def fourier(sample):
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs
    fft_abs = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
    return fft_abs


# Add max freq in a given second-long sample to time-freq table
# INPUT: Dict and list of fourier transform results, with len of num samples per second
# OUTPUT: None, adds key-value pair to dictionary
def max_freq(fft_abs, sec):
    max_fft_abs = max(fft_abs)
    dict_value = None
    for i in range(len(fft_abs)):  # Need to find which 1/10th of sec highest freq occurs
        if fft_abs[i] == max_fft_abs:
            tenth = float(i)/float(10)
            dict_value = float(sec) + tenth # !!!!!!!!!!!!!!!!!!!!!!!!!! NEED TO TRACK SECOND

    dict_key = round(max_fft_abs, 2) # Round freq to 2 decimal places
    return (dict_key, dict_value)



# Main method 
a1 = read_audio('Hiphopopotamus.wav')
a2 = create_samples(a1)
a3 = process_second(a2, 10)

b1 = read_audio('Hiphopopotamus.wav')
b2 = b1[44099:(44100*3)]
b3 = create_samples(b2)
b4 = process_second(b3, 10)

asorted2 = sorted(a3.items(), key=lambda x: x[1])
