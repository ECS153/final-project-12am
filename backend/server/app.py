from utils import (
    get_frames,
    clear_frames,
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
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'

app.config["UPLOAD_FOLDER"] = './media/video'
ALLOWED_EXTENSIONS = {'mov', 'mp4'}
THRESHOLD = 0.50
user_name = "Kenny"


@app.route('/')
def index():
    return 'Welcome to Lively'


@app.route('/create')
def create():
    analyzer = Analyzer(user_name)
    analyzer.create()
    return "Created Person Group."


trainer = Analyzer(user_name)


@app.route('/init')
def init_train():
    trainer.get_train_data()
    return "Get Trained Data ."


@app.route('/train')
def train():
    trainer.train()
    return "Trained Person Group."


@app.route('/delete')
def delete():
    analyzer = Analyzer(user_name)
    analyzer.delete()
    return "Deleted Person Group."


@app.route('/clear')
def clear():
    clear_frames(user_name)
    return "Clear all frames in folder 'data'"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    print('DEBUG: uploading file...')
    if request.method == 'POST':
        result = {}
        # Check username existence
        if 'username' not in request.form:
            flash("No username")
            result['result'] = 'False'
            return jsonify(result)
        username = request.form['username']
        print("DEBUG: username = ", username)
        # Check file existence
        if 'file' not in request.files:
            flash('No file part')
            result['result'] = 'False'
            return jsonify(result)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            result['result'] = 'False'
            return jsonify(result)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            clear_frames(username)
            get_frames(username, path)
            tester = Analyzer(username)
            is_me = False
            is_lively = tester.detect_liveness(path)
            if tester.identify() > THRESHOLD:
                is_me = True
            if is_me and is_lively:
                result['result'] = 'True'
            else:
                result['result'] = 'False'
            return jsonify(result)
            # return redirect(request.url)

    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
