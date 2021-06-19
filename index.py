import os
import hashlib
import tempfile
from exiftool import ExifTool
from flask import Flask, request, jsonify

app = Flask(__name__, template_folder="views", static_folder="public", static_url_path="/")
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024
secret = os.getenv("SECRET") or "BSidesTLV2021{This_Is_Not_The_Flag}"
if len(secret) < 35:
    raise Exception("Secret size should be 36 or above")


def parse_metadata(metadata, filter_keys=None):
    filter_keys = filter_keys or []
    parsed_metadata = {}
    for key, value in metadata.items():
        keys = key.split(":")

        o = parsed_metadata
        kl = len(keys)
        for i, k in enumerate(keys):
            if k not in o:
                o[k] = {}

            if i < kl - 1:
                o = o[k]
                continue

            o[k] = value

    for k in filter_keys:
        parsed_metadata.pop(k)

    return dict(parsed_metadata)


@app.route("/")
def index():
    return app.send_static_file('index.html')


@app.route("/view", methods=["POST"])
def view():
    token = request.form.get("token")
    if not token:
        return jsonify({"error": "empty token"})

    image = request.files.get("image")
    if not image:
        return jsonify({"error": "empty image"})

    if not image.mimetype.startswith("image/"):
        return jsonify({"error": "bad image"})

    image_stream = image.stream.read()
    mac = hashlib.sha1(secret.encode() + hashlib.sha1(image_stream).digest()).hexdigest()
    if token == mac:
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(image_stream)
                tmp.flush()
                tmp.close()

                with ExifTool() as et:
                    metadata = et.get_metadata(tmp.name)

                os.unlink(tmp.name)
        except Exception as ex:
            return jsonify({
                "error": str(ex)
            })

        return jsonify(parse_metadata(metadata, filter_keys=["File", "SourceFile"]))

    return jsonify({"error": "bad token"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
