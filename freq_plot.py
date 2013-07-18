import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
from pylab import *
from scipy import *

rate, data = scipy.io.wavfile.read('Hiphopopotamus.wav')  # Return the sample rate (in samples/sec) and data from a WAV file
print "RATE: ", rate
print "DATA: ", data[10000:20000]
print "DATA LEN: ", len(data)

data_test = data[:(rate*20)]
print "DATA TEST LEN: ", len(data_test)

data_lr_avg = []
for i in range(len(data_test)):
    average = (data_test[i][0] + data_test[i][1]) / 2
    data_lr_avg.append(average)

# print "DATA LR AVG: ", data_lr_avg
print "DATA LR AVG LEN: ", len(data_lr_avg)

data_lr_avg_sample = []
samples_sec = rate/10
for i in range(0, len(data_lr_avg), samples_sec):
    sample = data_lr_avg[i:i+samples_sec]
    sample_avg = sum(sample)/len(sample)
    data_lr_avg_sample.append(sample_avg)

print "DATA LR AVG SAMPLE: ", data_lr_avg_sample
print "DATA LR AVG SAMPLE LEN:", len(data_lr_avg_sample)

fft_data = np.fft.fft(data_lr_avg_sample)  # Compute the one-dimensional discrete Fourier Transform. (Returns complex values)
print "FFT DATA:", fft_data

fft_plot = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
print "FFT PLOT: ", fft_plot
# http://www.lomont.org/Software/Misc/FFT/SimpleFFT.pdf

# print 'LENGTH OF DATA PLOT: ', len(fft_plot)
# print "DATA TYPE: ", type(fft_plot)
# print "ELEMENT DATA TYPE: ", fft_plot.dtype


# # t = np.linspace(0,)
# # https://sites.google.com/site/haskell102/home/frequency-analysis-of-audio-file-with-python-numpy-scipy
plt.plot(fft_plot)
plt.show()




# pylab.specgram(fft_plot_sample)
