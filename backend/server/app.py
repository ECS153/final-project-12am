from utils import (
    get_frames,
    delete_frames,
)
from flask import (
    Flask,
    render_template,
)
from analyzer import Analyzer
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = set(['mov','mp4'])


# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'


# TODO: Configure for training/testing
user_name = "Linda"
analyzer = Analyzer(user_name)
THRESHOLD = 0.50


@app.route('/')
def index():
    print("start")
    get_frames(user_name)
    confidence = analyzer.identify()
    delete_frames()
    if analyzer.detect_liveness() and confidence > THRESHOLD:
        return 'Detect result: True'
    return 'Detect result: False'


@app.route('/create')
def create():
    analyzer.create()
    return "Created Person Group."


@app.route('/train')
def train():
    # Train with the videos upload
    get_frames(name)
    # Detect faces from the frames and add to Person Group
    analyzer.get_train_data()
    # Use the frames in the person group to train
    analyzer.train()
    return "Trained Person Group."

@app.route('/delete')
def delete():
    analyzer.delete()
    return "Deleted Person Group."

@app.route('/upload', methods=['GET','POST'])
def fileUpload():
    video = request.files['file']
    print("Video ", video)
    '''
    Classification and return the result here
    '''
    result = {'result': 'True'}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
