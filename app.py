import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import model

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    video1 = model.session.query(model.Track).get(1)
    video2 = model.session.query(model.Track).get(2)
    return render_template("index.html", video1=video1, video2=video2)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        if (file1 and allowed_file(file1.filename)) and (file2 and allowed_file(file2.filename)):
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)

            # save files info in db
            new_filename1 = filename1
            new_title = request.form.get("title")
            new_artist = request.form.get("artist")
            new_event = request.form.get("event")
            new_path = "static/videos/"
            new_file1 = model.Track(title=new_title, filename=new_filename1,
                                    artist=new_artist, event=new_event, path=new_path)
            model.session.add(new_file1)

            new_filename2 = filename2
            new_file2 = model.Track(title=new_title, filename=new_filename2,
                                    artist=new_artist, event=new_event, path=new_path)
            model.session.add(new_file2)

            model.session.commit()

            # upload file
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

            return redirect(url_for('uploaded_file', filename=filename1))

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
