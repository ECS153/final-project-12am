from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = set(['mov','mp4'])

@app.route('/')
def index():
    return "hello world!"

@app.route('/upload', methods=['GET','POST'])
def fileUpload():
    print(request.files['file'])
    return "Done"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
