from flask import Flask, render_template
import model

app = Flask(__name__)



@app.route('/')
def index():
    video1 = model.session.query(model.Track).get(1)
    video2 = model.session.query(model.Track).get(2)
    return render_template("index.html", video1=video1, video2=video2)

if __name__ == "__main__":
    app.run(debug=True)
