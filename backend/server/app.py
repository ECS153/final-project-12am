
from utils import get_frames

from flask import (
    Flask,
    render_template,
)
import os
import config
from analyzer import Analyzer

app = Flask(__name__)

# Set environment variables
# Flask App
# os.environ['FLASK_APP'] = 'app.py'
# os.environ['FLASK_ENV'] = 'development'

# # MS Face Recognition
# os.environ['FACE_SUBSCRIPTION_KEY'] = '50aaf75a5e464e1abb264a7aec7414c2'
# os.environ['FACE_ENDPOINT'] = 'https://mycsresourceface.cognitiveservices.azure.com/'

# FLASK_APP = config('FLASK_APP')
# FLASK_ENV = config('FLASK_ENV')


@app.route('/')
def index():
    print("start")
    # Trained, Identify ONLY
    # Person we are identifying (for testing purposes for now
    # since multiple people working on this)
    name = "Linda"
    analyzer = Analyzer(name)
    # get_frames(name)
    # Identify Only
    analyzer.identify()
    # analyzer.delete()
    # analyzer.verify()
    return "Good morning world!"


@app.route('/create')
def create():
    analyzer = Analyzer("Linda", 0)
    analyzer.create()
    return "Created Person Group"


@app.route('/train')
def train():
    name = "Linda"
    analyzer = Analyzer(name, 0)
    # Train with the videos upload
    # get_frames()
    # Detect faces from the frames and add to Person Group
    analyzer.get_train_data()
    # Use the frames in the person group to train
    analyzer.train_data()
    # analyzer.identify()
    # analyzer.verify()
    return "Good morning world!"

@app.route('/delete')
def delete():
    name = "Linda"
    analyzer = Analyzer(name, 0)
    analyzer.delete()
    return "Good morning world!"


if __name__ == "__main__":
    app.run(debug=True)


