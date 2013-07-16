import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt
from pylab import *
from scipy import *

rate, data = scipy.io.wavfile.read('Hiphopopotamus.wav')  # Return the sample rate (in samples/sec) and data from a WAV file
print "RATE: ", rate
print "DATA: ", data

data_sample = data[0:50000]

fft_data = np.fft.fft(data)  # Compute the one-dimensional discrete Fourier Transform. (Returns complex values)
print "FFT DATA:", fft_data

fft_plot = abs(fft_data)  # Taking abs value to get distance from zero (amplitude of frequency)
print 'LENGTH OF DATA PLOT: ', len(fft_plot)
print "DATA TYPE: ", type(fft_plot)
print "ELEMENT DATA TYPE: ", fft_plot.dtype

fft_plot_sample = fft_plot[0:50000]  #, 0]  # Testing subset of data
print "LENGTH OF DATA SAMPLE: ", len(fft_plot_sample)
print "DATA SAMPLE: ", fft_plot_sample

t = np.linspace(0,)
# https://sites.google.com/site/haskell102/home/frequency-analysis-of-audio-file-with-python-numpy-scipy
plt.plot(data_sample)
plt.show()




# pylab.specgram(fft_plot_sample)
