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
    output = "./" + filename[0] + "_1." + filename[1]
    call(["sox", audio_file, output, "channels", "1"])
    rate, data = scipy.io.wavfile.read(output)  # Return the sample rate (in samples/sec) and data from a WAV file
    # print "RATE: ", rate  # !! RETURN RATE
    return data


# sample span: length of sample (44100 is one second)
# overlap: number of data elements overlapping between samples
def process_audio(data, fft_bin_size, overlap):
    intensity_matrix = []

    # process first sample
    sample_data = data[0:fft_bin_size]
    if (len(sample_data) == fft_bin_size):
        freq_max = process_sample(sample_data)
        # frequency = round(freq_max, 2)
        # second = float((float(fft_bin_size)/2.0)/float(sample_rate))
        # time = round(second, 3)

        # freq_time_pairs.append((frequency, time))

    # process remainder of samples
    for i in range(int(fft_bin_size - overlap), len(data), int(fft_bin_size-overlap)):
        sample_data = data[i:i + fft_bin_size]
        if (len(sample_data) == fft_bin_size):
            freq_max = process_sample(sample_data)
            # frequency = round(freq_max, 2)
            # second = float((float(i) + float(fft_bin_size)/2.0)/float(sample_rate))
            # time = round(second, 3)

            # freq_time_pairs.append((frequency, time))

    return freq_time_pairs


# process individual sample
def process_sample(data):
    freq = fourier(data)
    return freq

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


# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
# Reference: http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
def fourier(sample):  #, overlap):
    fft_data = np.fft.fft(sample)  # Returns real and complex value pairs
    freqs = np.fft.fftfreq(len(sample))  #, overlap) #dont have to recalculate for each sample, pass as parameter
    mag = abs(fft_data) # not necessary
    mag2 = mag**2
    index = np.argmax(mag2)
    freq = freqs[index]  # only valid if index > len(fft_data)/2
    freq_hz = abs(freq*sample_rate)

    return freq_hz





def make_stereo(base_file, sample_file, sec_delay, dir):
    # trim base file
    base_input = base_file
    base_output1 = base_file.split(".")
    base_output2 = base_output1[1].split("/")
    base_output3 = base_output2[-1]

    base_output = dir + base_output3 + "_cut.wav"
    seconds = str(sec_delay)
    # seconds = str(float(sec_delay) * float(100))

    call(["sox", base_input, base_output, "trim", seconds])

    # combine L R channels
    sample_input = sample_file
    stereo_output = "stereo.wav"
    call(["sox", "-M", base_output, sample_input, stereo_output])

    return stereo_output


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
base0 = read_audio(sound_base)
print base0
base1 = base0
base2 = process_audio(base1, 1024, 1024*.0)
base3 = freq_list(base2)

sound_sample = extract_audio(dir, str(video2_sample))
sample0 = read_audio(sound_sample)
sample1 = sample0
sample2 = process_audio(sample1, 1024, 1024*.0)
print sample2
sample3 = freq_list(sample2)

start_points = find_start(base3, sample3, 6, 50) # 6, 50 has been working
print "start points:", start_points
alignment = best_start(base3, sample3, start_points)
print "alignment: ", alignment
secs = base2[alignment][1]  # must be longer sample
print "sec: ", secs


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








