#  How to track sample rate?
#  Create song class

import scipy.io.wavfile
import numpy as np
# import math.floor as floor


sample_rate = 44100


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(file):
    rate, data = scipy.io.wavfile.read(file)  # Return the sample rate (in samples/sec) and data from a WAV file
    print "RATE: ", rate
    return data


# num_keys is number of dictionary entries per second
def create_samples(data, num_keys):
    s = {}
    second = 0
    num_secs = round(len(data)/sample_rate, 0)
    num_keys_sec = sample_rate/num_keys
    for i in range(0, int(num_secs*sample_rate), num_keys_sec):
        s[second] = data[i:i+num_keys_sec]
        second += 1

    return s


# Process samples by second
# INPUT: Dictionary of seconds as keys and matrix of L R raw audio data as values
# OUTPUT: Returns dictionary of key(frequency) value(time) pairs
def process_sample(s, num):  #, num_samp_sec):
    d = {}
    # second = float(0)

    for i in range(len(s)):  # for second in song
        mono = channel_avg(s[i])
        split = split_samples(mono, num)
        fft = fourier(split)
        max = max_freq(fft, i, num)
        # second += float(1/num_samp_sec)

        if max[0] in d.keys() is not None:   # if dict key exists, append
            d[max[0]].append(max[1])  # dict_key is max freq and dict_value is time
        else:  # else create dict key and assign value
            d[max[0]] = max[1]

    return sorted(d.items(), key=lambda x: x[1])


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


# Split each second into x samples !!!!!!!!! SHOULD TAKE HIGHEST INSTEAD OF AVG?
# INPUT: list with length of sampling rate
# OUTPUT: list with length of number of indicated samples per second
def split_samples(mono_data, num_samp_sec):  # num samp sec is 20 if two samples per sec from create samples
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
def max_freq(fft_abs, sec, num):
    max_fft_abs = max(fft_abs)
    dict_value = None
    for i in range(len(fft_abs)):  # Need to find which 1/10th of sec highest freq occurs
        if fft_abs[i] == max_fft_abs:
            portion_of_sec = round((float(i)/float(num)), 2)
            dict_value = float(sec) + portion_of_sec

    dict_key = round(max_fft_abs, 2)  # Round freq to 2 decimal places
    return (dict_key, dict_value)


# Compare two value-sorted dictionary objects to see if d1 is an overlap/within d2
# INPUT: Two dictionaries, number of consecutive matches to be considered
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
            print 'MATCH NOT FOUND, INCREASE I, RESET J AND OFFSET'
            if prev_match is False:
                i += 1
            
            j = 0
            time_offset = None
            prev_match = False
            print "PREV MATCH: ", prev_match
            print ""

        if j == consec:
            print consec, "CONSECUTIVE MATCHES FOUND"
            return True

    print consec, 'CONSEC MATCHES NOT FOUND'
    return False


# Test
# Entire file
a1 = read_audio('Hiphopopotamus.wav')
# a2 = create_samples(a1, 2)
# a3 = process_second(a2, 10)

# Portion of file to compare
b1 = a1[0:44100*2]
b2 = create_samples(b1, 2)
b3 = process_second(b2, 10)

c1 = a1[0:700000]
c2 = create_samples(c1, 2)
c3 = process_second(c2, 10)



# compare(a3, b3, 3, 300)

