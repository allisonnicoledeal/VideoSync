import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
# from pylab import *
from scipy import *

rate, data = scipy.io.wavfile.read('Hiphopopotamus.wav')  # Return the sample rate (in samples/sec) and data from a WAV file
print "RATE: ", rate
print "DATA: ", data[10000:20000]  # taking sample of track
print "DATA LEN: ", len(data)

NUM_SAMP_SEC = 10

# Take one second sample of audio data
sec1 = data[0:44100]
print data[44000:44100]

# Average Left and right audio channels
data_lr_avg = []
for i in range(len(sec1)):
    average = (sec1[i][0] + sec1[i][1]) / 2
    data_lr_avg.append(average)

print "DATA_LR_AVG end of first second: ", data_lr_avg[44000:44100]

# Create 10 samples per second, take average of elemets 4410 at a time
sample = []
elements_per_sample = rate/NUM_SAMP_SEC
for j in range(0, len(data_lr_avg), (elements_per_sample)):
    added_elements = data_lr_avg[j:j+(elements_per_sample)]
    sample_avg = sum(added_elements)/len(added_elements)
    sample.append(sample_avg)
    print "SAMPLE AVG:", sample_avg

# Compute FFT 
fft_data = np.fft.fft(sample)  # Compute the one-dimensional discrete Fourier Transform. (Returns complex values)
print "FFT DATA:", fft_data

fft_abs = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
print "FFT ABS: ", fft_abs
max_fft_abs = max(fft_abs)
print "MAX FFT ABS:", max(fft_abs)

# Add entry to dictionary
d = {}
dict_key = max_fft_abs
print "DICT KEY: ", dict_key

if dict_key in d.keys() is not None:   # if dict key exists, append
    d[dict_key].append(i)  # k is frequency(key) and i is sample number(value)
else:  # else create dict key and assign value
    d[dict_key] = 1


print "DICTIONARY: ", d





