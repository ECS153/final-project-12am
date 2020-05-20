from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "hello world!"

@app.route('/upload', methods=['GET','POST'])
@cross_origin(origin='*',headers=['Content- Type'])
def testFunc():
    print("bla")
    return "hahahahaa"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
