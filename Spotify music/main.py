import json
import requests
import pandas as pd
from datetime import datetime
import datetime

import sqlalchemy
from sqlalchemy.orm import sessionmaker
import sqlite3
import psycopg2

from refresh import Refresh


spotify_token = ''


def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing exception")
        return False
    else:
        print("Some songs downloaded")

    # Primary Key Check
    if pd.Series(df['played_at']).is_unique:
        print("Primary Key 'played_at' Checked")
        pass
    else:
        raise Exception("Primary Key Check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null valued found")
    else:
        return True


def call_refresh():
    refreshCaller = Refresh()

    spotify_token = refreshCaller.refresh()
    print('Token refreshed\n')

    find_songs(spotify_token)


def find_songs(new_token):
    # if __name__ == "__main__":

    # Extract part of the ETL process

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=new_token)
    }

    # Convert time to Unix timestamp in milliseconds
    today = datetime.datetime.now()
    today_unix_timestamp = int(today.timestamp()) * 1000

    # Download all songs you've listened...
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&before={time}" \
                     .format(time=today_unix_timestamp), headers=headers)
    data = r.json()
    # print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:16])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    # Validate
    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")
    else:
        print("Data not valid")

    print(song_df)

    # Load
    engine = sqlalchemy.create_engine('postgresql://postgres:@localhost:5432/postgres')

    # try:
    connection = engine.connect()
    conn1 = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="",
        host="localhost",
        port="5432"
    )
    conn1.autocommit = True
    cursor = conn1.cursor()

    sql_query = """
        CREATE TABLE IF NOT EXISTS spotify.my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
        )
        """

    # query = connection.execute(sql_query)

    cursor.execute(sql_query)

    # tmp_df = pd.DataFrame({"song_name": ['1a'], "artist_name": ['2a'], "played_at": ['3a'], "timestamp": ['4a']})

    # CDC
    max_timestamp_in_db = engine.execute("SELECT MAX(timestamp) FROM spotify.my_played_tracks").fetchall()
    print(f"MAX timestamp in DB — {max_timestamp_in_db[0][0]}")

    # checking data in DB
    if max_timestamp_in_db[0][0] is not None:
        song_df = song_df[song_df.timestamp > max_timestamp_in_db[0][0]]

    if song_df.empty:
        print("Doesn't exist new data for load to DB")
    else:
        print(song_df)
        song_df.to_sql("my_played_tracks", engine, schema='spotify', index=False, if_exists='append')
        print("Data load to DB")

    # conn1.commit()
    conn1.close()
    print("Close database successfully")


call_refresh()
