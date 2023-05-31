from flask import Flask
from flask import render_template
from flask import request
import search_youtube
import json
import youtube_question
import uuid
import os

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def users():
    # 設定　url,query,id,txt
    
    url = request.form["url"]
    query = request.form["query"]
    id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
    txt_storage = f"./memory/{id}/"
    file_path = txt_storage+id+".txt"
    if query == "":
        query = "要約してください"
    if not os.path.exists(file_path):#ファイルがない場合に、テキストの作成、ベクトルデータの作成を行う
        txt = youtube_question.YoutubeText(url)
        os.mkdir(txt_storage)
        youtube_question.create_file(file_path,txt)
        youtube_question.setup_data("./storage/"+id,txt_storage)
        print("ベクトルデータの作成が完了しました")
    # gptにstorageにあるデータを投げて、queryに答えてもらう
    #TODO:大きなトークンで利用しようとすると、デフォルトの文章になってしまう
    #それは勘違いで、トークン数の大きい文章に圧迫されて、他の文章が表出していなかった。
    # storageを消しても結果が変わらなかったので、data_useの方に問題があると思われる。
    # data_useにファイルをまとめていたが、そうするとdata_use内にあるファイルをすべて利用してしまう。
    #フォルダを個別に指定することで、問題を解決した。
    re =youtube_question.question_gpt("./storage/"+id,query)
    print(re)
    return render_template("index.html",message = [re])


@app.route("/search",methods=["POST"])
def search():
    query=request.form["query"]
    re=search_youtube.get_video_info(query,3)
    return render_template("index.html",Youtube_txt = re)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)