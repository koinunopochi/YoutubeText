from dotenv import load_dotenv
load_dotenv()
import glob
import os
api_key=os.getenv('openai_api_key')

import uuid
from langchain.document_loaders import YoutubeLoader
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

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

  # ファイル名を作成
  id = str(uuid.uuid3(uuid.NAMESPACE_URL, url)) # urlからuuidを生成,urlが一致すれば同じuuidが生成される
  filename = id + ".txt"
  # ファイルの書き込み
  f = open("./storage/"+filename, 'w', encoding='UTF-8')
  f.write(data)
  f.close()
  return data # dataを返す

def ReserveGpt(docs): #gptに投げる前に、2000文字ごとに分割する
  encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
  tokens = encoding.encode(docs)
  tokens_count = len(tokens)
  print(f"token:{tokens_count}")
  #> token: 1000
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 2000,
      chunk_overlap  = 100,
      length_function = len,
  )
  split_docs = text_splitter.create_documents([docs])
  print(len(split_docs))
  return split_docs

def UseGpt(split_docs,query): #gptに投げて、要約をしてもらう
  # ここ自分で作成する方がよさそう、結果が悪い、すれっどかして、並列処理
  chatmodel = ChatOpenAI(openai_api_key=api_key ,model_name='gpt-3.5-turbo',temperature=0)
  chain = load_qa_chain(chatmodel, chain_type="map_reduce", return_map_steps=True)
  result =chain({"input_documents": split_docs, "question": query}, return_only_outputs=True)
  # print(result)
  return result

def glob_file(id):
  files = glob.glob("./storage/"+id+".txt")
  return files

def summary(url):
  id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
  if glob_file(id) == []:
    txt = YoutubeText(url)
  else:
    with open("./storage/"+id+".txt",encoding="UTF-8") as f:
      txt = f.read()
  # print(txt)
  split_docs = ReserveGpt(txt)
  # print(split_docs) # 1000文字ごとに分割されたリストを作成
  query = 'Youtubeから字幕データを取得したものです。要点を整理したものをリストにしたあと、要約してください'
  re_text=UseGpt(split_docs,query)
  # print(re_text)
  return re_text


def user_query(url,query):
  id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
  if glob_file(id) == []:
    txt = YoutubeText(url)
  else:
    with open("./storage/"+id+".txt",encoding="UTF-8") as f:
      txt = f.read()
  print(txt)
  split_docs = ReserveGpt(txt)
  # print(split_docs) # 1000文字ごとに分割されたリストを作成
  re_text=UseGpt(split_docs,query)
  return re_text

if __name__ == "__main__":
  summary("https://youtu.be/wdvclbIHfHk")