import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import StorageContext, load_index_from_storage, GPTVectorStoreIndex,LLMPredictor, ServiceContext,SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI

import uuid

from dotenv import load_dotenv
load_dotenv()
import os
#　設定
api_key=os.getenv('openai_api_key')
model = os.getenv('model_name')

from langchain.document_loaders import YoutubeLoader

def YoutubeText(url):#YouTubeの文字起こしファイルを作成する
  loader = YoutubeLoader.from_youtube_url(
    youtube_url=url,
    language="ja"
  )
  # ここで、loaderをインスタンス化
  docs = loader.load()
  content = docs[0].page_content
  return content

def create_file(filename,data):
  # ファイルの書き込み
  f = open(filename, 'w', encoding='UTF-8')
  f.write(data)
  f.close()
  print("done")

def setup_data(path,data_path):
  # 設定
  #data_path = "data_use"
  #path = "./storage"
  # LLM Predictor (gpt-3.5-turbo) + service context
  llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=api_key, temperature=0, model=model))
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
  # データの読み込み
  documents = SimpleDirectoryReader(data_path).load_data()
  # データから、ベクトルなどを作成
  index = GPTVectorStoreIndex.from_documents(
      documents, service_context=service_context
  )
  index.storage_context.persist(persist_dir= path)
  print("done")

def question_gpt(path,query):
  # 設定
  #path = "./storage"
  # LLM Predictor (gpt-3.5-turbo) + service context
  llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=api_key, temperature=0, model_name=model))
  service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=512)

  # rebuild storage context
  storage_context = StorageContext.from_defaults(persist_dir=path)
  # load index
  index = load_index_from_storage(storage_context, service_context=service_context)
  query_engine = index.as_query_engine(
      service_context=service_context,
  )
  print(path)
  print(query)
  response = query_engine.query("日本語で回答してください\n"+query)
  # print(response)
  return response


"""
if __name__ == "__main__":
  url = "https://www.youtube.com/watch?v=8ZtInClXe1Q"
  id = str(uuid.uuid3(uuid.NAMESPACE_URL, url))
  txt = YoutubeText(url)
  create_file("./data_use/"+id+".txt",txt)

  setup_data("./storage/"+id,"data_use")
  query = "この文章はどのようなことについて説明していますか。"
  question_gpt("./storage/"+id,query)
"""

