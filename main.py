from flask import Flask, request
from flask_cors import CORS, cross_origin
import os 
from lib import load_signal_from_file_path, find_notes
app = Flask(__name__)
CORS(app, supports_credentials=True)


# UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads\\')
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"wav"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
        y, fs = load_signal_from_file_path(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        notes = find_notes(y, fs)
        print(notes)

        return {
            "notes": notes
        }, 200
if __name__ == '__main__':
    app.run(debug=True)





