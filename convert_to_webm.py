# mp4 to webm: avconv -i ./static/videos/Business.mp4 -y BusinessWEBM.webm
from subprocess import call


def convert_video(mp4_video):
    video_name = mp4_video.split(".")
    webm_output = video_name[0] + "WEBM.webm"
    create_webm_file = call(["avconv", "-i", mp4_video, "-y", webm_output])  # -y: does not prompt for file overwrite

