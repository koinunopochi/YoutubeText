from llama_index import LLMPredictor, GPTVectorStoreIndex,ServiceContext,SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import os

# 設定
api_key=os.getenv('openai_api_key')
model = os.getenv('model_name')

# LLM Predictor (gpt-3.5-turbo) + service context
llm_predictor = LLMPredictor(llm=ChatOpenAI(openai_api_key=api_key, temperature=0, model=model))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=512)
# データの読み込み
documents = SimpleDirectoryReader('data_use').load_data()
# データから、ベクトルなどを作成
index = GPTVectorStoreIndex.from_documents(
    documents, service_context=service_context
)
index.storage_context.persist(persist_dir="./storage")
print("done")