#%%
from youtube_client import get_video_categories, get_trending_videos, get_channel_stats
from database import insert_categories, insert_videos, insert_channels
from datetime import datetime
from googleapiclient.errors import HttpError
import duckdb
from pathlib import Path

#%%

if __name__ == "__main__":

    BASE = Path(__file__).parent.parent
    output_path = BASE / "data"

    con = duckdb.connect(output_path / 'youtube.duckdb')

    # coleta as categorias de canais disponiveis com assignable = True
    
    categories_list = get_video_categories(region_code="BR")
    for category in categories_list:
        category["collect_date"] = datetime.today()

    # itera sobre a lista de categorias coletando o top 50 videos mais assistidos 
    # de cada categoria

    all_videos = []
    for category in categories_list:

        try:
            videos_list = get_trending_videos(category_id= category["id"], region_code= "BR")
            for i,video in enumerate(videos_list):
                video["trending_rank"] = i+1
                video["searched_id"] = category["id"]
                video["collect_date"] = datetime.today()
            all_videos.extend(videos_list)

        except HttpError:
            print(f"A categoria '{category["snippet"]["title"]}' (id {category["id"]}) foi pulada pois não existem videos em alta nela.")

    # coleta o canal de cada video, armazena em uma estrutura de dados e deduplica

    unique_channels = list({i["snippet"]["channelId"] for i in all_videos})

    # coleta as estatisticas de cada canal em batch

    channels_list = []
    for i in range(0,len(unique_channels),50):
        temporary_list = get_channel_stats(unique_channels[i:i + 50])
        channels_list.extend(temporary_list)

    for channel in channels_list:
        channel["collect_date"] = datetime.today()

    insert_categories(con = con, categories= categories_list)

    insert_videos(con = con, videos= all_videos)

    insert_channels(con = con, channels= channels_list)

    con.commit()
    con.close()

