#%%
from pathlib import Path
import duckdb

BASE = Path(__file__).parent.parent
output_path = BASE / "data"

con = duckdb.connect(output_path / 'youtube.duckdb')

sql_command = """

CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.channels (
    channel_id VARCHAR(100) PRIMARY KEY,
    channel_name VARCHAR(100),
    country VARCHAR(100),
    subscriber_count BIGINT,
    view_count BIGINT,
    video_count INTEGER,
    created_at TIMESTAMP,
    collected_at DATE
);

CREATE TABLE IF NOT EXISTS raw.videos (
    video_id VARCHAR(100),
    title VARCHAR(100),
    channel_id VARCHAR(100),
    category_id VARCHAR(100),
    searched_id VARCHAR(100),
    published_at TIMESTAMP,
    collected_at DATE,
    view_count BIGINT,
    like_count INTEGER,
    comment_count INTEGER,
    trending_rank INTEGER,
    region_code VARCHAR(100),

    PRIMARY KEY (video_id, searched_id, collected_at)
);

CREATE TABLE IF NOT EXISTS raw.categories (
    category_id VARCHAR(100) PRIMARY KEY, 
    category_name VARCHAR(100), 
    collected_at DATE
);
"""

con.execute(sql_command)
print("Tabela criada com sucesso.")

con.close()

def insert_videos(con, videos):

    sql = """INSERT OR IGNORE INTO raw.videos (
                                video_id, 
                                title, 
                                channel_id,
                                category_id,
                                searched_id,
                                published_at,
                                collected_at,
                                view_count,
                                like_count,
                                comment_count,
                                trending_rank,
                                region_code
                                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    for video in videos:
        con.execute(sql,[
                        video["id"], 
                        video["snippet"]["title"],
                        video["snippet"]["channelId"],
                        video["snippet"]["categoryId"],
                        video["searched_id"],
                        video["snippet"]["publishedAt"],
                        video["collect_date"],
                        int(value) if (value := video["statistics"].get("viewCount")) else None,
                        int(value) if (value := video["statistics"].get("likeCount")) else None,
                        int(value) if (value := video["statistics"].get("commentCount")) else None,
                        video["trending_rank"],
                        "BR"
                        ]
                    )
        
def insert_categories(con, categories):

    sql = """INSERT OR IGNORE INTO raw.categories (
                            category_id, 
                            category_name, 
                            collected_at)
                VALUES (?,?,?)"""

    for category in categories:            
        con.execute(sql, [
                        category["id"], 
                        category["snippet"]["title"], 
                        category["collect_date"]
                        ]
                    )
        
def insert_channels(con, channels):
    sql = """INSERT OR IGNORE INTO raw.channels (
                            channel_id,
                            channel_name,
                            country,
                            subscriber_count,
                            view_count,
                            video_count,
                            created_at,
                            collected_at)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
    for channel in channels:
        con.execute(sql, [
                        channel["id"],
                        channel["snippet"]["title"],
                        channel["snippet"].get("country"),
                        int(value) if (value := channel["statistics"].get("subscriberCount")) else None,
                        int(value) if (value := channel["statistics"].get("viewCount")) else None,
                        int(value) if (value := channel["statistics"].get("videoCount")) else None,
                        channel["snippet"]["publishedAt"],
                        channel["collect_date"]
                        ]
                    )