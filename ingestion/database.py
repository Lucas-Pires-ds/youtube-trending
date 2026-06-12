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
print("Tabela criada com sucesso (ou já existia).")

con.close()