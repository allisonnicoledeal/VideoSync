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

def youtube_to_mp4(youtube_link, song_title, dir):
    mp4_output = song_title + youtube_link[-11:] + ".mp4"
    output = "./" + dir + mp4_output
    call(["youtube-dl", "-o", output, youtube_link])
    print "youtube-dl", "-o", output, youtube_link
    return mp4_output



# youtube_to_mp4("http://www.youtube.com/watch?v=BdBxaRng4SU", "myFlorenceTest3", "uploads/")
