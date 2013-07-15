import numpy
import scipy.io.wavfile
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot

rate, data = scipy.io.wavfile.read('Hiphopopotamus.wav')
print "RATE: ", rate
print "DATA: ", data
data_bis = numpy.fft.ifft(numpy.fft.fft(data))
print "DATA_BIS: ", data_bis
print "DATA_BIS TYPE: ", data_bis.dtype

data_plot = abs(data_bis)
data_sample = data_plot[0:100000, 0]
print 'LENGTH OF DATA PLOT: ', len(data_plot)
print "ABS VALUE DATA: ", data_sample
print "DATA TYPE: ", type(data_sample)
print "ELEMENT DATA TYPE: ", data_sample.dtype


f = numpy.linspace(rate, len(data_sample), endpoint=False)
plt.plot(data_sample)
plt.show()
