from dotenv import load_dotenv
load_dotenv()
import os
api_key=os.getenv('openai_api_key')

from langchain.document_loaders import YoutubeLoader
import datetime
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

  # 日付の取得＿file nameに使う
  dt_now = datetime.datetime.now()
  filename = str(dt_now).replace(":", "_") + ".txt"
  # ファイルの書き込み
  f = open("./storage/"+filename, 'w', encoding='UTF-8')
  f.write(data)
  f.close()
  return data # dataを返す

def ReserveGpt(docs):
  encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
  tokens = encoding.encode(docs)
  tokens_count = len(tokens)
  print(f"token:{tokens_count}")
  #> token: 1000
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap  = 100,
      length_function = len,
  )
  split_docs = text_splitter.create_documents([docs])
  print(len(split_docs))
  return split_docs

def UseGpt(split_docs):
  chatmodel = ChatOpenAI(openai_api_key=api_key ,model_name='gpt-3.5-turbo',temperature=0)
  chain = load_qa_chain(chatmodel, chain_type="map_reduce", return_map_steps=True)

  query='要約してください'
  chain({"input_documents": split_docs, "question": query}, return_only_outputs=True)