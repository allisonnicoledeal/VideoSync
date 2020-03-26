from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from video_sync import model, youtube_downloads as convert, alignment_by_row_channels

UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"mp4"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def _process_file(file_, new_title, url):
    if file_ and allowed_file(file_.filename):
        new_filename = secure_filename(file_.filename)
        file_.save(os.path.join(app.config["UPLOAD_FOLDER"], new_filename))
        new_youtube_url = None
        new_thumbnail = None
    elif url:
        new_filename = convert.youtube_to_mp4(url, new_title, UPLOAD_FOLDER)
        new_youtube_url = "https://www.youtube.com/embed/" + url[-11:]
        new_thumbnail = convert.youtube_thumbnail(url)
    else:
        raise ValueError("Specify either a YouTube link or a file to upload")

    return new_filename, new_thumbnail, new_youtube_url


def _save_file(new_artist, new_event, new_filename, new_path, new_thumbnail, new_title, new_youtube_url):
    # new_filename_webm1 = convert.convert_video(filename1, UPLOAD_FOLDER)  # convert file to webm
    new_filename_webm1 = "webmfilename"
    new_file = model.Track(title=new_title, filename=new_filename, artist=new_artist, event=new_event, path=new_path,
                           filename_webm=new_filename_webm1, youtube_url=new_youtube_url,
                           thumbnail_url=new_thumbnail)
    model.session.add(new_file)
    return new_file


def _save_analysis(delay, new_file, new_group_id):
    new_track_id = new_file.id
    new_sync_point = delay[0]
    new_analysis = model.Analysis(group_id=new_group_id, track_id=new_track_id, sync_point=new_sync_point)
    model.session.add(new_analysis)


def _post():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")

    new_title = request.form.get("title")
    new_artist = request.form.get("artist")
    new_event = request.form.get("event")
    new_path = UPLOAD_FOLDER

    url1 = request.form.get("url1")
    url2 = request.form.get("url2")

    filename1, thumbnail1, new_url1 = _process_file(file1, new_title, url1)
    filename2, thumbnail2, new_url2 = _process_file(file2, new_title, url2)

    try:
        new_file1 = _save_file(new_artist, new_event, filename1, new_path, thumbnail1, new_title, new_url1)
        new_file2 = _save_file(new_artist, new_event, filename2, new_path, thumbnail2, new_title, new_url2)

        # save group info into db
        new_timestamp = datetime.datetime.now()
        new_group = model.Group(timestamp=new_timestamp)
        model.session.add(new_group)

        model.session.flush()

        # analyze delay
        delay = alignment_by_row_channels.align(filename1, filename2, UPLOAD_FOLDER)
        # delay = (0, 5)

        # save analysis into db
        new_group_id = new_group.id
        _save_analysis(delay, new_file1, new_group_id)
        _save_analysis(delay, new_file2, new_group_id)

        model.session.commit()
    except Exception as e:
        model.session.rollback()
        raise e

    return redirect("/watch?group_id=" + str(new_group.id))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return _post()
    else:
        video1 = model.session.query(model.Track).get(11)
        video2 = model.session.query(model.Track).get(12)
        groups = model.session.query(model.Group).all()
        return render_template("index.html", video1=video1, video2=video2, groups=groups)


@app.route("/watch", methods=["GET", "POST"])
def watch():
    if request.method == "POST":
        return _post()
    else:
        group_id = request.args.get("group_id")
        video_group = model.session.query(model.Group).get(group_id)
        groups = model.session.query(model.Group).all()
        return render_template("watch.html", video_group=video_group, groups=groups)
