from utils import (
    get_frames,
    delete_frames,
)
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    jsonify,
)
from analyzer import Analyzer
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'

app.config["UPLOAD_FOLDER"] = './media/test'
ALLOWED_EXTENSIONS = {'mov', 'mp4'}

# TODO: Configure for training/testing
user_name = "Linda"
analyzer = Analyzer(user_name)
THRESHOLD = 0.50


def detect():
    print("start")
    get_frames(user_name)
    analyzer.create()
    analyzer.train()
    confidence = analyzer.identify()
    delete_frames()
    analyzer.delete()
    if confidence > THRESHOLD:
        return 'Detect result: True'
    # if analyzer.detect_liveness() and confidence > THRESHOLD:
    #     return 'Detect result: True'
    return 'Detect result: False'


@app.route('/')
def index():
    #detect()
    return 'Welcome to Lively'


@app.route('/create')
def create():
    analyzer.create()
    return "Created Person Group."


@app.route('/train')
def train():
    # Train with the videos upload
    get_frames(user_name)
    # Detect faces from the frames and add to Person Group
    analyzer.get_train_data()
    # Use the frames in the person group to train
    analyzer.train()
    return "Trained Person Group."


@app.route('/delete')
def delete():
    analyzer.delete()
    return "Deleted Person Group."



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    print('DEBUG: uploading file...')
    if request.method == 'POST':
        # Check file existence
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print('DEBUG: filename = ', file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('DEBUG: file saved!',filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            analyzer.detect_liveness(path)
            # detect()
            # return redirect(request.url)
            '''
            Classification and return the result here
            '''
            result = {'result': 'True'}
            return jsonify(result)

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
