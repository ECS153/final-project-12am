
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
    # Trained, Identify ONLY
    analyzer = Analyzer()
    get_frames()
    # Identify Only
    analyzer.get_test_data()
    # analyzer.verify()
    return "Good morning world!"

@app.route('/train')
def train():
    analyzer = Analyzer()
    # Train with the videos upload
    get_frames()
    # Detect faces from the frames and add to Person Group
    analyzer.get_train_data()
    # Use the frames in the person group to train
    analyzer.train_data()
    analyzer.get_test_data()
    # analyzer.verify()
    return "Good morning world!"

if __name__ == "__main__":
    app.run(debug=True)


