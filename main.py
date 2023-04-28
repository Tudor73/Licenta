from flask import Flask, request
from flask_cors import CORS, cross_origin
import os 
from lib import load_signal_from_file_path, find_notes, find_maximum_amplitude, map_notes_to_fretboard
import subprocess
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
CORS(app, supports_credentials=True)




basedir = os.path.abspath(os.path.dirname(__file__))

# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads\\')
UPLOAD_FOLDER = "uploads/"
SAVED_FOLDER = "uploads/saved"
ALLOWED_EXTENSIONS = {"wav"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAVED_FOLDER'] = SAVED_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


# db model
class Track(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    track_name = db.Column(db.String(50), nullable=False)
    # track_path = db.Column(db.String(50), nullable=False)
    # track_notes_path = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Track %r>' % self.track_name


app.app_context().push()

path = os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav")

ffmpeg_path = 'C:/Program Files/FFmpeg/bin/ffmpeg.exe'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
@cross_origin()
def process_audio():
    if 'file' not in request.files:
        return {"error": "No file1"}, 400
    file = request.files['file']
    if file.filename == '':
        return {"error": "No file"}, 400
    if file:

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        # new_file = moviepy.VideoFileClip(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        # file_name = file.filename.split(".")[0]
        # new_file.audio.write_audiofile(os.path.join(app.config['UPLOAD_FOLDER'], file_name + ".wav"))

        y, fs = load_signal_from_file_path(os.path.join(app.config['UPLOAD_FOLDER'],  file.filename))
        maxim = find_maximum_amplitude(y)
        notes = find_notes(y, fs, maxim)
        # os.remove (os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        print(notes)
        frets = map_notes_to_fretboard(notes)
        print(frets)

        return {
            "notes": frets
        }, 200

@app.route('/upload-audio', methods=['POST'])
@cross_origin()
def upload_audio():
        try:
            path = os.path.join(app.config['UPLOAD_FOLDER'], "audio.wav")
            audio_data = request.get_data()
            with open(path, 'wb') as f:
                f.write(audio_data)

            command = [ffmpeg_path, '-y', '-i', path, '-acodec', 'pcm_s16le', '-ar', str(44100), os.path.join(app.config['UPLOAD_FOLDER'], "audio_modified.wav")]
            subprocess.call(command)
            # return 'Audio file saved successfully', 200
        except Exception as e:
            print(e)
            return 'Error saving audio file', 500


        y, fs = load_signal_from_file_path(os.path.join(app.config['UPLOAD_FOLDER'], "audio_modified.wav"))
        maxim = find_maximum_amplitude(y)
        notes = find_notes(y, fs, maxim)

        print(notes)
        return {"notes": notes}, 200

@app.route('/save', methods=['POST'])
@cross_origin()
def save(): 
    fileName = request.get_json()['fileName']
    folderName = fileName[:fileName.index(".")]
    track = Track(username="test", track_name=folderName)
    db.session.add(track)
    db.session.commit()
    os.makedirs(os.path.join(app.config['SAVED_FOLDER'], folderName), exist_ok=True)
    Path(os.path.join(app.config['UPLOAD_FOLDER'], fileName)).rename(os.path.join(app.config['SAVED_FOLDER'], folderName, fileName))
    return {"res":"saved"}, 200


if __name__ == '__main__':
    app.run(debug=True)



