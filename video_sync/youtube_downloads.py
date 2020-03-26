from __future__ import absolute_import, division, print_function, unicode_literals

from subprocess import call

import envoy
import os.path


# working examples:
# mp4 to webm: avconv -i ./static/videos/Business.mp4 -y BusinessWEBM.webm
# avconv -i ./uploads/Business.mp4 -y ./uploads/BusinessTest.webm
# avconv -ss 00:00:15 -t 00:00:48 -i HipVsRhy.mp4 -codec copy HipClip.mp4

def convert_video(mp4_video, dir_):
    video_name = mp4_video.split(".")
    webm_output = video_name[0] + "WEBM.webm"
    input_ = os.path.join(dir_, mp4_video)
    output = os.path.join(dir_, webm_output)
    call(["ffmpeg", "-i", input_, "-y", output])  # generate webm file (-y: does not prompt for file overwrite)
    return webm_output


def youtube_to_mp4(youtube_link, song_title, dir_):
    mp4_output = song_title + youtube_link[-11:] + ".mp4"
    output = os.path.join(dir_, mp4_output)
    call(["youtube-dl", "-o", output, youtube_link])
    print("youtube-dl", "-o", output, youtube_link)
    return mp4_output


def youtube_thumbnail(youtube_link):
    output = envoy.run("youtube-dl --get-thumbnail " + youtube_link)
    output_str = output.std_out
    return output_str

# thumb = youtube_thumbnail("https://www.youtube.com/watch?v=Z5PPlk53IMY")
# youtube_to_mp4("https://www.youtube.com/watch?v=BdBxaRng4SU", "myFlorenceTest3", "uploads/")
