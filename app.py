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
        if file1 and allowed_file(file1.filename):
            # upload file
            filename1 = secure_filename(file1.filename)
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

            # save file info in db
            new_filename1= filename1
            new_title1 = request.args.get("title1")
            new_artist1 = request.args.get("artist1")
            new_file1 = model.Track(title=new_title1, filename=new_filename1, artist=new_artist1)
            model.session.add(new_file1)
            model.session.commit()

            return redirect(url_for('uploaded_file', filename=filename1))

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
