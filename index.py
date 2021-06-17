from flask import Flask, request, render_template

app = Flask(__name__, template_folder="views", static_folder="public", static_url_path="/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view", methods=["POST"])
def view():
    token = request.form.get("token")
    image = request.files.get("image")
    print(token, image)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
