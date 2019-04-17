import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from user_agents import parse


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)
    # check data quality
    df.fillna(0, inplace=True)

    # insert song record
    song_data = (df['song_id'].values[0], df['title'].values[0],
                 df['artist_id'].values[0], int(df['year'].values[0]),
                 float(df['duration'].values[0]))

    cur.execute(song_table_insert, song_data)
    # insert artist record
    artist_data = (df['artist_id'].values[0], df['artist_name'].values[0],
                   str(df['artist_location'].values[0]),
                   float(df['artist_latitude'].values[0]),
                   float(df['artist_longitude'].values[0]))

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)
    # check data quality
    df.fillna(0, inplace=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    time_data = (df.ts, t.dt.hour, t.dt.day,
                 t.dt.week, t.dt.month,
                 t.dt.year, t.dt.dayofweek)

    column_labels = ('start_time', 'hour', 'day',
                     'week', 'mounth', 'year',
                     'weekday')

    date_dict = {}
    for i in range(0, len(column_labels)):
        date_dict[column_labels[i]] = time_data[i].astype('int')

    time_df = pd.DataFrame.from_dict(date_dict)
    time_df = time_df.drop_duplicates(keep='first')

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    users_table = {'userId': df.userId.values,
                   'first_name': df.firstName.values,
                   'last_name': df.lastName.values,
                   'gender': df.gender.values,
                   'level': df.level.values}

    user_df = pd.DataFrame(data=users_table)
    user_df = user_df.drop_duplicates(keep='first')

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level,
                         songid, artistid, row.sessionId,
                         row.location, row.userAgent)

        cur.execute(songplay_table_insert, songplay_data)

    # insert useragent record

    ua = df.userAgent

    # get unique records from current file
    ua = list(set(ua))

    # parse user_agent data
    for row in ua:
        user_agent = parse(row)

        if user_agent.os.version_string:
            os_version = user_agent.os.version_string
        else:
            os_version = None
            
        if (user_agent.os.family == 'Linux'):
            os_family = 'Other Linux'
        else:
            os_family = user_agent.os.family

        user_agent_data = (row, user_agent.browser.family,
                           user_agent.browser.version_string,
                           os_family, os_version, user_agent.is_mobile)

        cur.execute(useragent_table_insert, user_agent_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 \
                            dbname=sparkifydb \
                            user=student \
                            password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
