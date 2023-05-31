from apiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv('google_api_key')

# Youtube API settings
API_KEY = api_key
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=API_KEY
)

def get_video_info(keyword,max_num):
    # search settings
    youtube_query = youtube.search().list(
        part='id,snippet', #取得する情報の種類、現在はすべて
        q=keyword,# 検索したいキーワード
        type='video',#検索クエリの条件を指定
        maxResults=max_num,#最大50件
        order='relevance',# 検索結果のソート手段
    )
    """
    【orderオプション】
      date – リソースを作成日の新しい順に並べます。
      rating – リソースを評価の高い順に並べます。
      relevance – リソースを検索クエリの関連性が高い順に並べます。このパラメータのデフォルト値です。
      title – リソースをタイトルのアルファベット順に並べます。
      videoCount – アップロード動画の番号順（降順）にチャンネルを並べます。
      viewCount – リソースを再生回数の多い順に並べます。
    """

    # execute()で検索を実行
    youtube_response = youtube_query.execute()

    # 検索結果を取得し、リターンする
    return youtube_response.get('items', [])


  
if __name__ == "__main__":
    result =get_video_info("python",5)
    #for i in range(len(result)):
     #  print("https://www.youtube.com/watch?v="+result[i]["id"]["videoId"])
    #data = json.dumps(result, indent=2)
    #print(data)