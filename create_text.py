from langchain.document_loaders import YoutubeLoader
import datetime

def YoutubeText(url):
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

  # 日付の取得＿file nameに使う
  dt_now = datetime.datetime.now()
  filename = str(dt_now).replace(":", "_") + ".txt"
  # ファイルの書き込み
  f = open("./storage/"+filename, 'w', encoding='UTF-8')
  f.write(data)
  f.close()
  return data # dataを返す

