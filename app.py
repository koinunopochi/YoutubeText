from flask import Flask
from flask import render_template
from flask import request
import create_text
import search_youtube
import json

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def users():
    url = request.form["url"]
    query = request.form["query"]
    if query == "":
      txt = create_text.summary(url)
    else:
      txt= create_text.user_query(url,query)
    text =""
    for i in range(len(txt["intermediate_steps"])):
      text +=txt["intermediate_steps"][i]+"\n"
    text = text +txt["output_text"]
    txt_ary = text.splitlines()
    return render_template("index.html",message = txt_ary)

@app.route("/search",methods=["POST"])
def search():
    query=request.form["query"]
    re=search_youtube.get_video_info(query,3)
    return render_template("index.html",Youtube_txt = re)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)