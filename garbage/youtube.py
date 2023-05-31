from dotenv import load_dotenv
load_dotenv()
import glob
import os
api_key=os.getenv('openai_api_key')

import uuid
from langchain.document_loaders import YoutubeLoader

def YoutubeText(url):#YouTubeの文字起こしファイルを作成する
  loader = YoutubeLoader.from_youtube_url(
    youtube_url=url,
    language="ja"
  )
  # ここで、loaderをインスタンス化
  docs = loader.load()
  content = docs[0].page_content
  # 空白で改行
  data = content.replace(" ","\n")
  print(data)
  # ファイル名を作成
  id = str(uuid.uuid3(uuid.NAMESPACE_URL, url)) # urlからuuidを生成,urlが一致すれば同じuuidが生成される
  filename = id + ".txt"
  # ファイルの書き込み
  f = open("./data_use/"+filename, 'w', encoding='UTF-8')
  f.write(data)
  f.close()
  return data # dataを返す

def glob_file(id):
  files = glob.glob("./data_use/"+id+".txt")
  return files

if __name__ == "__main__":
  summary("https://youtu.be/wdvclbIHfHk")