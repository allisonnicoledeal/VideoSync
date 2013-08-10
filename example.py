import wave
import struct
import numpy as np

if __name__=='__main__':
    data_size=40000
    fname="test.wav"
    frate=11025.0 
    wav_file=wave.open(fname,'r')
    data=wav_file.readframes(data_size)
    wav_file.close()
    data=struct.unpack('{n}h'.format(n=data_size), data)
    data=np.array(data)

    w = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(w))
    print(freqs.min(),freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx=np.argmax(np.abs(w)**2)
    freq=freqs[idx]
    freq_in_hertz=abs(freq*frate)
    print(freq_in_hertz)