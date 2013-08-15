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
    call(["avconv", "-y", "-i", dir+video_file, "-vn", "-f", "wav", output])
    # audio_data = call(["avconv", "-n", "-i", dir+video_file, "-vn", "-f", "wav", output])
    return output


# Read file
# INPUT: Audio file
# OUTPUT: Sets sample rate of wav file, Returns data read from wav file (numpy array of integers)
def read_audio(audio_file):

    filename = audio_file.split(".")
    print 'FILENAME: ', filename
    output = "./" + filename[0] + "_1." + filename[1]
    # output = "." + filename[1] + "_1." + filename[2]
    call(["sox", audio_file, output, "channels", "1"])
    rate, data = scipy.io.wavfile.read(output)  # Return the sample rate (in samples/sec) and data from a WAV file
    # print "RATE: ", rate  # !! RETURN RATE
    return data


# sample span: length of sample (44100 is one second)
# overlap: number of data elements overlapping between samples
def generate_matrix(data, fft_bin_size, overlap):
    intensity_matrix = []

    # process first sample and set matrix height
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
    for i in range(len(fft_data)/2):
        r = fft_data[i].real**2
        j = fft_data[i].imag**2
        mag.append(round(math.sqrt(r+j),2))
        # mag.append(math.log(abs(fft_data[i])))

    # freqs = np.fft.fftfreq(len(sample))
    # freq = freqs[index]  # only valid if index > len(fft_data)/2
    # freq_hz = abs(freq*sample_rate)

    return mag


# def make_bins(intensity_matrix, zone_height, zone_width):
#     samples = []
#     for i in range(int(len(intensity_matrix[0])/zone_width)):
#         for j in range(int(len(intensity_matrix)/zone_height)):
#             bin_data = []
#             for k in range(zone_height):
#                 x_min = i * zone_width
#                 x_max = (i+1) * zone_width
#                 y = (j * zone_height) + k
#                 section = intensity_matrix[y][x_min:x_max]
#                 bin_data.append()




# def find_bin_peaks():

def find_peaks(intensity_matrix, zone_height, zone_width, num_samples, fft_bin_size):  #num samples per zone
    peaks = []  # tuples of time and freq
    freqs = np.fft.fftfreq(len(intensity_matrix))  #, overlap) #dont have to recalculate for each sample, pass as parameter


    # Define zone
    for i in range(int(len(intensity_matrix[0])/zone_width)):
        # print "i: ", i
        for j in range(int(len(intensity_matrix)/zone_height)):
            # Find max num_samples in zone
            zone_max = [(0, 0, 0)]
            if (i * zone_width) < len(intensity_matrix[0]):

                for k in range(zone_height):
                    x_min = i * zone_width
                    x_max = (i+1) * zone_width
                    y = (j * zone_height) + k
                    section = intensity_matrix[y][x_min:x_max]
                    # if ((i == 0) and (j==0)):
                    # print "i ", i
                    # print "j ", j
                    # print "x min: ", x_min
                    # print "x max: ", x_max
                    # print "y: ", y
                    # print "section:", section
                    max_int = max(section)
                    # print "max intensity: ", max_int

                    while (max_int > (min(zone_max))[0]):
                        # print "zone max: ", zone_max

                        x = (i * zone_width) + section.index(max_int)  # x coordinate
                        # print "x coord: ", x
                        second = round((float((x*fft_bin_size)+((x+1)*fft_bin_size))/float(2.0))/float(sample_rate),2)
                        y = (j * zone_height) + k  # y coordinate
                        # print "y coord: ", y
                        frequency = freqs[y]
                        zone_max.append((max_int, x, y)) # replace it with larger tuple
                        # zone_max.append((max_int, frequency, second)) # replace it with larger tuple
                        section.remove(max_int)  # delete maximum element
                        # print "section: ", section

                        # print len(zone_max)

                        if (len(zone_max) > num_samples):
                            zone_max.remove(min(zone_max)) # remove smallest number
                        # print "zone_max: ", zone_max

                        if len(section) > 0:
                            max_int = max(section)  # find new max in sample
                        # print "new max int: ", max_int
                        else:
                            max_int = 0
                    # print ""
            # print "zone max: ", zone_max
            peaks.append(zone_max)


    return peaks


def make_peaks_list(peaks):
    peaks_list = []
    for i in range(len(peaks)):
        for j in range(len(peaks[0])):
            peaks_list.append(peaks[i][j])
    return peaks_list



def plot_peaks(peak_tuples_list):
    x = []
    y = []

    for i in range(len(peak_tuples_list)):
        for j in range(len(peak_tuples_list[0])):
            x.append(peak_tuples_list[i][j][1])
            y.append(peak_tuples_list[i][j][2])
    # plt.plot(x,y,'kx')
    # plt.show()

    return x, y


def time_diff(peak_list_base, peak_list_sample, err):
    time_deltas= {}
    for i in range(len(peak_list_sample)):
        for j in range(len(peak_list_base)):
            # if freqs match
            if ((peak_list_sample[i][2] < peak_list_base[j][2] + err) and (peak_list_sample[i][2] > peak_list_base[j][2] - err)):  # tuple is (intensity, x(time), y(freq))
                # calculate time difference
                time_diff = peak_list_sample[i][1] - peak_list_base[j][1]
                #if dictionary entry, 
                if time_diff in time_deltas.keys():
                    # add one to number of instances time differenc occurs
                    time_deltas[time_diff] += 1
                # else
                else:
                    # create new dict entry w value of 1
                    time_deltas[time_diff] = 1
    return time_deltas




def time_diff2(peak_list_base, peak_list_sample, err):
    time_deltas = {}
    base_frequencies = {} # key: freq, values is (x)
    for i in range(len(peak_list_base)):
        if peak_list_base[i][2] in base_frequencies.keys():
            base_frequencies[peak_list_base[i][2]].append(peak_list_base[i][1])
        else:
            base_frequencies[peak_list_base[i][2]] = [peak_list_base[i][1]]
    for j in range(len(peak_list_sample)):
        if peak_list_sample[j][2] in base_frequencies.keys():  # check if in base freqs
            for k in range(len(base_frequencies.get(peak_list_sample[j][2]))):
                time_diff = peak_list_sample[j][1] - base_frequencies[peak_list_sample[j][2]][k]
                if time_diff in time_deltas.keys():
                    time_deltas[time_diff] += 1
                else:
                    time_deltas[time_diff] = 1
    return time_deltas




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
    plt.plot(x_base, y_base, 'ko')
    plt.title('Base')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.subplot(2, 1, 2)
    plt.plot(x_sample, y_sample, 'ko')
    plt.title('Sample')
    plt.xlabel('Time')
    plt.ylabel('Frequency')

    plt.show()




# video1_base = "regina6POgShQ-lC4.mp4"
# v1 = "regina6POgShQ-lC4.mp4"
# video2_sample = "reginaJo2cUWpILMg.mp4"
# v2 = "reginaJo2cUWpILMg.mp4"
# v2 = "tessalateoGIjeYNlOXE.mp4" # sample
# v1 = "tessalateBLZQmqJ6Yos.mp4" # base
# v1 = "Settle2d_tj-9_dGog.mp4"
# v2 = "Settle2kFaZIKtcn6s.mp4"

# directory="./uploads/"

def align(video1_base, video2_sample, dir):


    # TESTS
    sound_b = extract_audio(dir, str(video1_base))
    audio_b = read_audio(sound_b)
    matrix_b = generate_matrix(audio_b[44100*10:44100*110], 1024, 1024*0)
    peaks_b = find_peaks(matrix_b, 80, 80, 20, 1024)
    peaks_list_b = make_peaks_list(peaks_b)
    print "peaks list b done"


    sound_s = extract_audio(dir, str(video2_sample))
    audio_s = read_audio(sound_s)
    matrix_s = generate_matrix(audio_s[44100*10:44100*110], 1024, 1024*0)
    peaks_s = find_peaks(matrix_s, 80, 80, 20, 1024)
    peaks_list_s = make_peaks_list(peaks_s)
    print "peaks list s done"

    # offsets = time_diff(peaks_list_b, peaks_list_s, 3)
    # offsets_sorted = sorted(offsets.items(), key=lambda x: x[1])
    # print "offset sorting done"
    # print offsets_sorted

    offsets2 = time_diff2(peaks_list_b, peaks_list_s, 3)
    offsets_sorted2 = sorted(offsets2.items(), key=lambda x: x[1])
    print "offset sorting done"
    print offsets_sorted2

    # delay = offsets_sorted[-1]
    # print delay
    delay2 = offsets_sorted2[-1]
    print delay2

    # x_b, y_b = plot_peaks(peaks_b)
    # plt.subplot(2, 1, 1)
    # plt.plot(x_b, y_b, 'kx')
    # x_s, y_s = plot_peaks(peaks_s)
    # plt.subplot(2, 1, 2)
    # plt.plot(x_s, y_s, 'kx')

    # plt.show()

    if delay2[0] > 0:
        return (float(delay2[0])/43, 0)
    else:
        return (0, abs(float(delay2[0])/43))


# delta_t = align(v1, v2, directory)
# print delta_t

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








