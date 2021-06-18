from flask import Flask, request
from tempfile import TemporaryFile
# import pyexiftool

app = Flask(__name__)

# @app.route('/<image>/<image_hash>')
# def index():
#     result = ''.join((random.choice(string.ascii_lowercase) for x in range(255))
#     f = request.files['image']
#     f.save('./')@app.route('/<image>/<image_hash>')
# def index():
#     result = ''.join((random.choice(string.ascii_lowercase) for x in range(255))
#     f = request.files['image']
#     f.save('./')
@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)