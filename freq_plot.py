#  How to track sample rate?
#  Create song class

import scipy.io.wavfile
import numpy as np
from subprocess import call
# import math.floor as floor


sample_rate = 44100

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
def parse_samples(data, fft_bin_size, overlap):
    s = {}

    sample_no = 0
    s[sample_no] = data[0:fft_bin_size]
    sample_no += 1

    for i in range(int(fft_bin_size - overlap), len(data), fft_bin_size):
        s[sample_no] = data[i:i + fft_bin_size]
        print "SAMPLE NO", sample_no
        print "SPAN: ", fft_bin_size
        print "SHOUD MATCH SAMPLE SPAN", len(s[sample_no])
        sample_no += 1

    return s


# Process samples by second
# INPUT: Dictionary of seconds as keys and matrix of L R raw audio data as values
# OUTPUT: Returns dictionary of key(frequency) value(time) pairs
def process_sample(s, num, fft_bin_size):  #, num_samp_sec):
    d = {}
    second = float(0)

    for i in range(len(s)):  # for second in song
        mono = channel_avg(s[i])
        # split = split_samples(mono, num)
        fft = fourier(mono)
        max = max_freq(fft)  # (fft, i, num)

        # second += float(((fft_bin_size * i) - (fft_bin_size/2))/sample_rate)
        # FIX THIS PART!

        if max in d.keys() is not None:   # if dict key exists, append
            d[max].append(second)  # dict_key is max freq and dict_value is time
        else:  # else create dict key and assign value
            d[max] = [second]

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


# Split each second into x samples !!!!!!!!! SHOULD TAKE HIGHEST INSTEAD OF AVG?
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
def fourier(sample):
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs
    fft_abs = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
    return fft_abs


# Add max freq in a given second-long sample to time-freq table
# INPUT: Dict and list of fourier transform results, with len of num samples per second
# OUTPUT: value of maximum frequency
def max_freq(fft_abs):  #, sec, num):
    max_fft_abs = max(fft_abs)
    return max_fft_abs


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
fftbin = 1024
# Entire file

sound = extract_audio("HipVsRhy.mp4")
a1 = read_audio("HipVsRhyWAV.wav")

# a2 = create_samples(a1, 2)
# a3 = process_second(a2, 10)

# Portion of file to compare
# b1 = a1[0:44100*2]
# b2 = parse_samples(b1, 1024, 1024*.75)
# b3 = process_sample(b2, 1024, 1024)
# b4 = sorted(b3.items(), key=lambda x: x[1])

c1 = a1[0:700000]
c2 = parse_samples(c1, 1024, 1024*.75)
c3 = process_sample(c2, 1024, 1024)
c4 = sorted(c3.items(), key=lambda x: x[1])



# compare(a3, b3, 3, 300)

