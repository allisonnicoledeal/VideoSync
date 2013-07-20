import numpy as np
import scipy.io.wavfile
# import matplotlib.pyplot as plt
# from pylab import *
from scipy import *

rate, data = scipy.io.wavfile.read('Hiphopopotamus.wav')  # Return the sample rate (in samples/sec) and data from a WAV file
print "RATE: ", rate
print "DATA: ", data[10000:20000]  # taking sample of track
print "DATA LEN: ", len(data)

num_samp_sec = 10
num_samp = 2
data_test = data[:(rate*num_samp_sec*2)]
print "DATA TEST LEN: ", len(data_test)

data_lr_avg = []
for i in range(len(data_test)):
    average = (data_test[i][0] + data_test[i][1]) / 2
    data_lr_avg.append(average)

# print "DATA LR AVG: ", data_lr_avg
print "DATA LR AVG LEN: ", len(data_lr_avg)

d = {}


section_dict = {}

for i in range(0, len(data_lr_avg)/rate/num_samp_sec, 1):
    section_dict[i] = None

# for j in range(len(section_dict)):
#     for k in range(num_samp_sec):
#             section_dict[j] = data_lr_avg[k:k+num_samp_sec]

# # for i in range(0, len(data_lr_avg), rate/num_samp_sec):
# #     section_dict[i] = data_lr_avg[i:i+num_samp_sec]

print "EMPTY DICT:", section_dict
print "LEN SECTION DICT: ", len(section_dict)

i = 0
for j in range(0, len(data_lr_avg), rate*num_samp_sec):
    section_dict[i] = data_lr_avg[j:j+(rate*num_samp_sec)]
    i += 1

 # ===========================================
for i in range(0, len(section_dict)):  # WHOLE SONG # i is sample number, s1, s2, etc.
    sample = []
    # print len(section_dict[i])
    for j in range(0, len(section_dict[i]), (rate/num_samp_sec)):
        # print section_dict[i][j]
        added_elements = section_dict[i][j:j+(rate/num_samp_sec)]
        print len(added_elements)
        # sample_avg = sum(added_elements)/len(added_elements)
        # print sample_avg
        # sample.append(section_dict[i][j])

    print "SAMPLE LENGTH:", len(sample), "SHOULD EQUAL", num_samp_sec

#     fft_data = np.fft.fft(sample)  # Compute the one-dimensional discrete Fourier Transform. (Returns complex values)
#     print "FFT DATA:", fft_data

#     fft_abs = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
#     print "FFT ABS: ", fft_abs
#     max_fft_abs = max(fft_abs)
#     print "MAX FFT ABS:", max(fft_abs)

#     dict_key = max_fft_abs
#     print "DICT KEY: ", dict_key

#     if dict_key in d.keys() is not None:   # if dict key exists, append
#         d[dict_key].append(i)  # k is frequency(key) and i is sample number(value)
#     else:  # else create dict key and assign value
#         d[dict_key] = i


# print "DICTIONARY: ", d

 # ===========================================

# data_lr_avg_sample = []
# samples_sec = rate/10
# for i in range(0, len(data_lr_avg), samples_sec):
#     sample = data_lr_avg[i:i+samples_sec]

#     sample_avg = sum(sample)/len(sample)
#     data_lr_avg_sample.append(sample_avg)

# data_lr_avg_sample = []
# samples_sec = rate/10
# for i in range(0, len(data_lr_avg), samples_sec):
#     sample = data_lr_avg[i:i+samples_sec]

#     sample_avg = sum(sample)/len(sample)
#     data_lr_avg_sample.append(sample_avg)

# print "DATA LR AVG SAMPLE: ", data_lr_avg_sample
# print "DATA LR AVG SAMPLE LEN:", len(data_lr_avg_sample)

# fft_data = np.fft.fft(data_lr_avg_sample)  # Compute the one-dimensional discrete Fourier Transform. (Returns complex values)
# print "FFT DATA:", fft_data

# fft_plot = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
# print "FFT PLOT: ", fft_plot
# http://www.lomont.org/Software/Misc/FFT/SimpleFFT.pdf

# print 'LENGTH OF DATA PLOT: ', len(fft_plot)
# print "DATA TYPE: ", type(fft_plot)
# print "ELEMENT DATA TYPE: ", fft_plot.dtype


# # t = np.linspace(0,)
# # # https://sites.google.com/site/haskell102/home/frequency-analysis-of-audio-file-with-python-numpy-scipy
# plt.plot(fft_plot)
# plt.show()




# pylab.specgram(fft_plot_sample)
