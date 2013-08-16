#  How to track sample rate?
#  Create song class
# http://www.dspguide.com/
# Reference: http://stackoverflow.com/questions/3694918/how-to-extract-frequency-associated-with-fft-values-in-python
# http://dsp.stackexchange.com/questions/1262/creating-a-spectrogram

# AUDIO FINGERPRINTING: http://www.nhchau.com/files/AudioFingerprint-02-FP04-2.pdf
# http://www.mtg.upf.edu/files/publications/MMSP-2002-pcano.pdf
# http://159.226.42.3/doc/2008/A%20Robust%20Feature%20Extraction%20Algorithm%20for%20Audio%20Fingerprinting.pdf
# http://www.satnac.org.za/proceedings/2011/papers/Software/181.pdf

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
    # output = "./" + filename[0] + "_1." + filename[1] # web app
    output = "." + filename[1] + "_1." + filename[2] # testing
    call(["sox", audio_file, output, "channels", "1"])
    rate, data = scipy.io.wavfile.read(output)  # Return the sample rate (in samples/sec) and data from a WAV file
    # print "RATE: ", rate  # !! RETURN RATE
    return data


def max_intensities(data, fft_bin_size, overlap, box_width, box_height, num_maxes):
    box_maximums = {}
    # process first sample
    box_x = 0
    bin_data = data[0:fft_bin_size]
    if (len(bin_data) == fft_bin_size):
        intensities = fourier(bin_data)
        for i in range(len(intensities)):
            box_y = i/box_height
            if box_maximums.has_key((box_x, box_y)):
                if len(box_maximums[(box_x, box_y)]) < num_maxes: 
                    box_maximums[(box_x, box_y)].append((intensities[i], 0, i))  # tuple of (intensity, x, y), x represents time, y represents freq
                elif (intensities[i] > min(box_maximums[(box_x, box_y)])[0]):  # check if current intensity is higher than lowest stored intensity
                    box_maximums[(box_x, box_y)].append((intensities[i], 0, i))
                    box_maximums[(box_x, box_y)].remove(min(box_maximums[(box_x, box_y)]))
            else:
                box_maximums[(box_x, box_y)] = [(intensities[i], 0, i)]
    # process remainder of samples)
    j_counter = 1
    for j in range(int(fft_bin_size - overlap), len(data), int(fft_bin_size-overlap)):
        print "j_counter :", j_counter
        box_x = j_counter/box_width
        print "box_x:", box_x
        bin_data = data[j:j + fft_bin_size]
        if (len(bin_data) == fft_bin_size):
            intensities = fourier(bin_data)
            for k in range(len(intensities)):
                box_y = k/box_height
                if box_maximums.has_key((box_x, box_y)):
                    if len(box_maximums[(box_x, box_y)]) < num_maxes: 
                        box_maximums[(box_x, box_y)].append((intensities[k], j, k))  # tuple of (intensity, x, y), x represents time, y represents freq
                    elif (intensities[k] > min(box_maximums[(box_x, box_y)])[0]):  # check if current intensity is higher than lowest stored intensity
                        box_maximums[(box_x, box_y)].append((intensities[k], j, k))
                        box_maximums[(box_x, box_y)].remove(min(box_maximums[(box_x, box_y)]))
                else:
                    box_maximums[(box_x, box_y)] = [(intensities[k], j, k)]
            j_counter += 1
    return box_maximums


# Compute the one-dimensional discrete Fourier Transform
# INPUT: list with length of number of samples per second
# OUTPUT: list of real values len of num samples per second
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







def dict_to_list(dict):
    freqs_list = []

    for key in dict.keys():
        for i in range(len(key)):
            freqs_list.append(dict[key][i])
    return freqs_list


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
                if time_deltas.has_key(time_diff):
                    time_deltas[time_diff] += 1
                else:
                    time_deltas[time_diff] = 1
    return time_deltas




# def plot_freq(base_freqs, sample_freqs):  # argument is list of freq-time tuples
#     x_base = []
#     y_base = []
#     x_sample = []
#     y_sample = []

#     for i in range(len(base_freqs)):
#         x_base.append(base_freqs[i][1])
#         y_base.append(base_freqs[i][0])

#     for j in range(len(sample_freqs)):
#         x_sample.append(sample_freqs[j][1])
#         y_sample.append(sample_freqs[j][0])

#     x_sample.append(max(x_base))
#     y_sample.append(max(y_base))




#     plt.subplot(2, 1, 1)
#     plt.plot(x_base, y_base, 'ko')
#     plt.title('Base')
#     plt.xlabel('Time')
#     plt.ylabel('Frequency')

#     plt.subplot(2, 1, 2)
#     plt.plot(x_sample, y_sample, 'ko')
#     plt.title('Sample')
#     plt.xlabel('Time')
#     plt.ylabel('Frequency')

#     plt.show()




video1_base = "regina6POgShQ-lC4.mp4"
# v1 = "regina6POgShQ-lC4.mp4"
video2_sample = "reginaJo2cUWpILMg.mp4"
# v2 = "reginaJo2cUWpILMg.mp4"
# v2 = "tessalateoGIjeYNlOXE.mp4" # sample
# v1 = "tessalateBLZQmqJ6Yos.mp4" # base
# v1 = "Settle2d_tj-9_dGog.mp4"
# v2 = "Settle2kFaZIKtcn6s.mp4"

dir="./uploads/"

sound_b = extract_audio(dir, str(video1_base))
audio_b = read_audio(sound_b)
maxes_b = max_intensities(audio_b[44100*0:44100*20], 1024, 0, 43, 128, 2)
list_b = dict_to_list(maxes_b)

sound_s = extract_audio(dir, str(video2_sample))
audio_s = read_audio(sound_s)
maxes_s = max_intensities(audio_s[44100*5:44100*15], 1024, 0, 43, 128, 2)
list_s = dict_to_list(maxes_s)

offsets2 = time_diff2(list_b, list_s, 3)
offsets_sorted2 = sorted(offsets2.items(), key=lambda x: x[1])
# print "offset sorting done"
print offsets_sorted2
                        # data, fft_bin_size, overlap, box_width, box_height, num_maxes
print maxes_b


def align(video1_base, video2_sample, dir):
    # TESTS
    sound_b = extract_audio(dir, str(video1_base))
    audio_b = read_audio(sound_b)
    maxes_b = max_intensities(audio_b)
    list_b = dict_to_list(maxes_b)

    sound_s = extract_audio(dir, str(video2_sample))
    audio_s = read_audio(sound_s)
    maxes_s = max_intensities(audio_s[:44100*10])
    list_s = dict_to_list(maxes_s)

    offsets2 = time_diff2(list_b, list_s, 3)
    offsets_sorted2 = sorted(offsets2.items(), key=lambda x: x[1])
    # print "offset sorting done"
    print offsets_sorted2


    # matrix_b = generate_matrix(audio_b[44100*10:44100*110], 1024, 1024*0)
    # peaks_b = find_peaks(matrix_b, 80, 80, 20, 1024)
    # peaks_list_b = make_peaks_list(peaks_b)
    # print "peaks list b done"


    # sound_s = extract_audio(dir, str(video2_sample))
    # audio_s = read_audio(sound_s)
    # matrix_s = generate_matrix(audio_s[44100*10:44100*110], 1024, 1024*0)
    # peaks_s = find_peaks(matrix_s, 80, 80, 20, 1024)
    # peaks_list_s = make_peaks_list(peaks_s)
    # print "peaks list s done"

    # offsets = time_diff(peaks_list_b, peaks_list_s, 3)
    # offsets_sorted = sorted(offsets.items(), key=lambda x: x[1])
    # print "offset sorting done"
    # print offsets_sorted

    # offsets2 = time_diff2(peaks_list_b, peaks_list_s, 3)
    # offsets_sorted2 = sorted(offsets2.items(), key=lambda x: x[1])
    # print "offset sorting done"
    # print offsets_sorted2

    # # delay = offsets_sorted[-1]
    # # print delay
    # delay2 = offsets_sorted2[-1]
    # print delay2

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



        #TEST METHODS

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


stereo = mame



