from flask import Flask
from flask import render_template
from flask import request
from create_text import YoutubeText

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def users():
    url = request.form["url"]
    print("POST:"+url)
    # Youtubeをテキスト化
    txt = YoutubeText(url)
    txt_ary = txt.splitlines()
    return render_template("index.html",message = txt_ary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)