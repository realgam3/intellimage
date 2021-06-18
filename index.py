from flask import Flask, request, render_template, jsonify
from hashlib import sha1
from os import environ
from exiftool import *
from tempfile import NamedTemporaryFile 

app = Flask(__name__, template_folder="views", static_folder="public", static_url_path="/")
secret = environ['SECRET'] if "SECRET" in environ.keys() else "bae"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view", methods=["POST"])
def view():
    imagehash = sha1()
    our_hash = sha1()

    token = request.form.get("token")
    image = request.files.get("image")
    image_stream = image.stream.read()

    imagehash.update(image_stream)
    our_hash.update(secret.encode('utf-8') + imagehash.hexdigest().encode('utf-8'))
  
    if (our_hash.hexdigest() == token):
      with NamedTemporaryFile() as tmp:
        tmp.write(image_stream)
        with ExifTool() as et:
          metadata = et.get_metadata(tmp.name)
          return metadata
    return jsonify({})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
