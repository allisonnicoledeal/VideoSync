import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import model
import convert_to_webm as convert
import datetime
import alignment_by_row_channels


UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    # video1 = model.session.query(model.Track).get(55)
    # video2 = model.session.query(model.Track).get(56)
    video1 = model.session.query(model.Track).get(11)
    video2 = model.session.query(model.Track).get(12)
    groups = model.session.query(model.Group).all()

    if request.method == 'POST':

        # if (request.files['file1'] and request.files['file2']):
        #     print "in if statement"
        #     file1 = request.files['file1']
        #     file2 = request.files['file2']
        file1 = None
        file2 = None

        new_title = request.form.get("title")
        new_artist = request.form.get("artist")
        new_event = request.form.get("event")
        new_path = UPLOAD_FOLDER

        # file upload
        if (file1 and allowed_file(file1.filename)) and (file2 and allowed_file(file2.filename)):
            new_filename1 = secure_filename(file1.filename)
            new_filename2 = secure_filename(file2.filename)

            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename2))

        # youtube link upload
        elif (request.form.get("url1") and request.form.get("url2")):
            url1 = request.form.get("url1")
            url2 = request.form.get("url2")
            new_filename1 = convert.youtube_to_mp4(url1, new_title, UPLOAD_FOLDER)
            new_filename2 = convert.youtube_to_mp4(url2, new_title, UPLOAD_FOLDER)
            new_youtube_url1 = "http://www.youtube.com/embed/" + url1[-11:]
            new_youtube_url2 = "http://www.youtube.com/embed/" + url2[-11:]
            new_thumbnail1 = convert.youtube_thumbnail(url1)
            new_thumbnail2 = convert.youtube_thumbnail(url2)
            
        # save file 1
        # new_filename_webm1 = convert.convert_video(filename1, UPLOAD_FOLDER)  # convert file to webm
        new_filename_webm1 = "webmfilename"
        new_file1 = model.Track(title=new_title, filename=new_filename1,
                                artist=new_artist, event=new_event, path=new_path,
                                filename_webm=new_filename_webm1, youtube_url=new_youtube_url1, thumbnail_url=new_thumbnail1)
        model.session.add(new_file1)

        # save file 2
        # new_filename_webm2 = convert.convert_video(filename2, UPLOAD_FOLDER)  # convert file to webm
        new_filename_webm2 = "webmfilename"
        new_file2 = model.Track(title=new_title, filename=new_filename2,
                                artist=new_artist, event=new_event, path=new_path,
                                filename_webm=new_filename_webm2, youtube_url=new_youtube_url2, thumbnail_url=new_thumbnail2)
        model.session.add(new_file2)

        # save group info into db
        new_timestamp = datetime.datetime.now()
        new_group = model.Group(timestamp=new_timestamp)
        model.session.add(new_group)

        model.session.flush()

        # analyze delay
        delay = alignment_by_row_channels.align(new_filename1, new_filename2, UPLOAD_FOLDER)
        # delay = (0, 5)

        # save analysis into db
        new_group_id = new_group.id
        new_track_id1 = new_file1.id
        new_sync_point1 = delay[0]
        new_analysis1 = model.Analysis(group_id=new_group_id, track_id=new_track_id1,
                                       sync_point=new_sync_point1)
        model.session.add(new_analysis1)

        new_track_id2 = new_file2.id
        new_sync_point2 = delay[1]
        new_analysis2 = model.Analysis(group_id=new_group_id, track_id=new_track_id2,
                                       sync_point=new_sync_point2)
        model.session.add(new_analysis2)

        model.session.commit()


        return redirect('/watch?group_id=' + str(new_group.id))

    return render_template("index.html", video1=video1, video2=video2, groups=groups)


@app.route('/watch', methods=['GET', 'POST'])
def watch():
    group_id = request.args.get("group_id")
    video_group = model.session.query(model.Group).get(group_id)
    groups = model.session.query(model.Group).all()

    if request.method == 'POST':

        # if (request.files['file1'] and request.files['file2']):
        #     print "in if statement"
        #     file1 = request.files['file1']
        #     file2 = request.files['file2']
        file1 = None
        file2 = None

        new_title = request.form.get("title")
        new_artist = request.form.get("artist")
        new_event = request.form.get("event")
        new_path = UPLOAD_FOLDER

        # file upload
        if (file1 and allowed_file(file1.filename)) and (file2 and allowed_file(file2.filename)):
            new_filename1 = secure_filename(file1.filename)
            new_filename2 = secure_filename(file2.filename)

            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename2))

        # youtube link upload
        elif (request.form.get("url1") and request.form.get("url2")):
            url1 = request.form.get("url1")
            url2 = request.form.get("url2")
            new_filename1 = convert.youtube_to_mp4(url1, new_title, UPLOAD_FOLDER)
            new_filename2 = convert.youtube_to_mp4(url2, new_title, UPLOAD_FOLDER)
            new_youtube_url1 = "http://www.youtube.com/embed/" + url1[-11:]
            new_youtube_url2 = "http://www.youtube.com/embed/" + url2[-11:]
            new_thumbnail1 = convert.youtube_thumbnail(url1)
            new_thumbnail2 = convert.youtube_thumbnail(url2)
            
        # save file 1
        # new_filename_webm1 = convert.convert_video(filename1, UPLOAD_FOLDER)  # convert file to webm
        new_filename_webm1 = "webmfilename"
        new_file1 = model.Track(title=new_title, filename=new_filename1,
                                artist=new_artist, event=new_event, path=new_path,
                                filename_webm=new_filename_webm1, youtube_url=new_youtube_url1, thumbnail_url=new_thumbnail1)
        model.session.add(new_file1)

        # save file 2
        # new_filename_webm2 = convert.convert_video(filename2, UPLOAD_FOLDER)  # convert file to webm
        new_filename_webm2 = "webmfilename"
        new_file2 = model.Track(title=new_title, filename=new_filename2,
                                artist=new_artist, event=new_event, path=new_path,
                                filename_webm=new_filename_webm2, youtube_url=new_youtube_url2, thumbnail_url=new_thumbnail2)
        model.session.add(new_file2)

        # save group info into db
        new_timestamp = datetime.datetime.now()
        new_group = model.Group(timestamp=new_timestamp)
        model.session.add(new_group)

        model.session.flush()

        # analyze delay
        delay = alignment_by_row_channels.align(new_filename1, new_filename2, UPLOAD_FOLDER)
        # delay = (0, 5)

        # save analysis into db
        new_group_id = new_group.id
        new_track_id1 = new_file1.id
        new_sync_point1 = delay[0]
        new_analysis1 = model.Analysis(group_id=new_group_id, track_id=new_track_id1,
                                       sync_point=new_sync_point1)
        model.session.add(new_analysis1)

        new_track_id2 = new_file2.id
        new_sync_point2 = delay[1]
        new_analysis2 = model.Analysis(group_id=new_group_id, track_id=new_track_id2,
                                       sync_point=new_sync_point2)
        model.session.add(new_analysis2)

        model.session.commit()

        return redirect('/watch?group_id=' + str(new_group.id))

    return render_template("watch.html", video_group=video_group, groups=groups)


if __name__ == "__main__":
    app.run(debug=True)

