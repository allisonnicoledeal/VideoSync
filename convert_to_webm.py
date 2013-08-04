# mp4 to webm: avconv -i ./static/videos/Business.mp4 -y BusinessWEBM.webm
# avconv -ss 00:00:15 -t 00:00:48 -i HipVsRhy.mp4 -codec copy HipClip.mp4

from subprocess import call


def convert_video(mp4_video):
    video_name = mp4_video.split(".")
    webm_output = video_name[0] + "WEBM.webm"
    create_webm_file = call(["avconv", "-i", mp4_video, "-y", webm_output])  # -y: does not prompt for file overwrite

