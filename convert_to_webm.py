# working examples
    # mp4 to webm: avconv -i ./static/videos/Business.mp4 -y BusinessWEBM.webm
    # avconv -i ./uploads/Business.mp4 -y ./uploads/BusinessTest.webm
    # avconv -ss 00:00:15 -t 00:00:48 -i HipVsRhy.mp4 -codec copy HipClip.mp4

from subprocess import call


def convert_video(mp4_video, dir):
    video_name = mp4_video.split(".")
    webm_output = video_name[0] + "WEBM.webm"
    input = "./" + dir + mp4_video
    output = "./" + dir + webm_output
    call(["avconv", "-i", input, "-y", output])  # generate webm file (-y: does not prompt for file overwrite)
    # call(["avconv", "-i", input, " ", output])  # generate webm file (-y: does not prompt for file overwrite)
    return webm_output
