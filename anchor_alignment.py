#  How to track sample rate?
#  Create song class
# http://www.dspguide.com/

# generate thumbnails: ffmpeg -i input.flv -an -ss 1:00:00 -r 1 -vframes 1 -f mjpeg -y output.jpg

import scipy.io.wavfile
from scipy import stats
import numpy as np
from numpy import arange
from subprocess import call
import math
import matplotlib.pyplot as plt

sample_rate = 44100

# Extract audio from video file, save as wav auido file
# INPUT: Video file
# OUTPUT: Does not return any values, but saves audio as wav file
def extract_audio(dir, video_file):
    track_name = video_file.split(".")
    audio_output = track_name[0] + "WAV.wav"  # !! CHECK TO SEE IF FILE IS IN UPLOADS DIRECTORY
    output = dir + audio_output
    call(["avconv", "-i", dir+video_file, "-vn", "-f", "wav", output])
    # audio_data = call(["avconv", "-n", "-i", dir+video_file, "-vn", "-f", "wav", output])
    return output


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(audio_file):

    filename = audio_file.split(".")
    print 'FILENAME: ', filename
    # output = "./" + filename[0] + "_1." + filename[1]
    output = "." + filename[1] + "_1." + filename[2]
    call(["sox", audio_file, output, "channels", "1"])
    rate, data = scipy.io.wavfile.read(output)  # Return the sample rate (in samples/sec) and data from a WAV file
    # print "RATE: ", rate  # !! RETURN RATE
    return data


# sample span: length of sample (44100 is one second)
# overlap: number of data elements overlapping between samples
def generate_matrix(data, fft_bin_size, overlap):
    intensity_matrix = []

    # process first sample
    sample_data = data[0:fft_bin_size]
    if (len(sample_data) == fft_bin_size):
        intensities = fourier(sample_data)
        for j in range(len(intensities)): # equivalent to len(bin size)
            intensity_matrix.append([intensities[j]])

    # process remainder of samples
    for i in range(int(fft_bin_size - overlap), len(data), int(fft_bin_size-overlap)):
        sample_data = data[i:i + fft_bin_size]
        if (len(sample_data) == fft_bin_size):
            intensities = fourier(sample_data)
            for k in range(len(intensities)):
                intensity_matrix[k].append(intensities[k])


    return intensity_matrix




# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
# Reference: http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
# http://dsp.stackexchange.com/questions/1262/creating-a-spectrogram

# AUDIO FINGERPRINTING: http://www.nhchau.com/files/AudioFingerprint-02-FP04-2.pdf
# http://www.mtg.upf.edu/files/publications/MMSP-2002-pcano.pdf
# http://159.226.42.3/doc/2008/A%20Robust%20Feature%20Extraction%20Algorithm%20for%20Audio%20Fingerprinting.pdf
# http://www.satnac.org.za/proceedings/2011/papers/Software/181.pdf


def fourier(sample):  #, overlap):
    mag = []
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs
    for i in range(len(fft_data)):
        r = fft_data[i].real**2
        j = fft_data[i].imag**2
        mag.append(math.sqrt(r+j))

    # freqs = np.fft.fftfreq(len(sample))
    # freq = freqs[index]  # only valid if index > len(fft_data)/2
    # freq_hz = abs(freq*sample_rate)

    return mag








def plot_freq(base_freqs, sample_freqs):  # argument is list of freq-time tuples
    x_base = []
    y_base = []
    x_sample = []
    y_sample = []

    for i in range(len(base_freqs)):
        x_base.append(base_freqs[i][1])
        y_base.append(base_freqs[i][0])

    for j in range(len(sample_freqs)):
        x_sample.append(sample_freqs[j][1])
        y_sample.append(sample_freqs[j][0])

    x_sample.append(max(x_base))
    y_sample.append(max(y_base))




    plt.subplot(2, 1, 1)
    plt.plot(x_base, y_base, 'ko-')
    plt.title('Base')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    plt.plot(x_sample, y_sample, 'ko-')
    plt.title('Sample')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.show()






video1_base = "regina6POgShQ-lC4.mp4"
video2_sample = "reginaJo2cUWpILMg.mp4"
dir="./uploads/"

# def align(video1_base, video2_sample, dir):
sound_base = extract_audio(dir, str(video1_base))
audio_base = read_audio(sound_base)
matrix_base = generate_matrix(audio_base, 1024, 1024*.25)
# base3 = freq_list(base2)

# sound_sample = extract_audio(dir, str(video2_sample))
# sample0 = read_audio(sound_sample)
# sample1 = sample0
# sample2 = generate_matrix(sample1, 1024, 1024*.0)
# print sample2
# sample3 = freq_list(sample2)

# start_points = find_start(base3, sample3, 6, 50) # 6, 50 has been working
# print "start points:", start_points
# alignment = best_start(base3, sample3, start_points)
# print "alignment: ", alignment
# secs = base2[alignment][1]  # must be longer sample
# print "sec: ", secs


# stereo = make_stereo(sound_base, sound_sample, secs, dir)
# print stereo

# plot_freq(base2, sample2)

# return (0, secs)
    

#========== TESTING============

# # video1_base = "Gold.mp4"
# # video2_sample = "HipClip.mp4"
# v1 = "ReginaPrayerYaTFoYVGWBk.mp4"
# v2 = "ReginaPrayerDUtDOS-7mkg.mp4"
# v1 = "regina6POgShQ-lC4.mp4"
# v2 = "reginaJo2cUWpILMg.mp4"
# video1_base = "Gold.mp4"
# video2_sample = "Gold.mp4"
# video2_sample = "Reg2.mp4"
# v2 = "tessalateoGIjeYNlOXE.mp4" # sample
# v1 = "tessalateBLZQmqJ6Yos.mp4" # base

# secs, sound_base, b0, b1, b2, b3, sound_sample, s0, s1, s2, s3, start_points, alignment= align(v1, v2, "./uploads/")






#========== TEST ================
# offset = analyze("regina6POgShQ-lC4.mp4", "reginaJo2cUWpILMg.mp4", "./uploads/")
# offset = analyze("Reg1.mp4", "Reg2.mp4")
# offset = analyze("HipVsRhy.mp4", "HipClip.mp4")

# http://www.youtube.com/watch?v=6POgShQ-lC4
# http://www.youtube.com/watch?v=Jo2cUWpILMg
# http://www.youtube.com/watch?v=FKbWPHRCJm8
# http://www.youtube.com/watch?v=R49i0BzIiHc








