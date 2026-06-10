#%%
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if API_KEY is None:
    raise ValueError("API KEY incorreta")

youtube = build("youtube", "v3", developerKey=API_KEY)


def get_video_categories(region_code):
    data = (youtube.videoCategories()
                        .list(part="snippet", 
                            regionCode=region_code)
                            .execute()
            )["items"]
    assignable_filtered = [i for i in data if i["snippet"]["assignable"]]

    return assignable_filtered


def get_trending_videos(category_id, region_code):
    data = (youtube.videos()
                        .list(part="snippet, statistics", 
                            chart = "mostPopular", 
                            regionCode=region_code, 
                            videoCategoryId=category_id, 
                            maxResults=50)
                            .execute()
            )
    return data["items"]

def get_channel_stats(channel_ids):
    channel_ids_string = ",".join(channel_ids)
    data = (youtube.channels()
            .list(part="snippet, statistics",
                  id = channel_ids_string)
            .execute()
            )
    return data["items"]
