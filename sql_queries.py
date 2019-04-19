# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"
useragent_table_drop = "DROP TABLE IF EXISTS useragent"

# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS \
                         songplays (songplay_id serial PRIMARY KEY, \
                         start_time bigint NOT NULL, user_id int NOT NULL, \
                         level varchar NOT NULL, song_id varchar, \
                         artist_id varchar, session_id int NOT NULL, \
                         location varchar NOT NULL, \
                         user_agent varchar NOT NULL);")

user_table_create = ("CREATE TABLE IF NOT EXISTS \
                      users (user_id int PRIMARY KEY, first_name varchar, \
                      last_name varchar, gender varchar, \
                      level varchar NOT NULL);")

song_table_create = ("CREATE TABLE IF NOT EXISTS \
                     songs (song_id varchar PRIMARY KEY, \
                     title varchar NOT NULL, \artist_id varchar, \
                     year int, duration decimal NOT NULL);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS \
                       artists (artist_id varchar PRIMARY KEY, \
                       name varchar NOT NULL, location varchar, \
                       lattitude decimal, longitude decimal);")

time_table_create = ("CREATE TABLE IF NOT EXISTS \
                     time (start_time bigint PRIMARY KEY, hour int, day int,\
                     week int, month int, year int, weekday int);")

useragent_table_create = ("CREATE TABLE IF NOT EXISTS \
                          useragent (user_agent varchar PRIMARY KEY, \
                          browser varchar,browser_version varchar, \
                          os varchar, os_version varchar,\
                          mobile varchar);")

# INSERT RECORDS

songplay_table_insert = ("INSERT INTO \
                         songplays (start_time, user_id, level,\
                         song_id, artist_id, session_id, location,\
                         user_agent)VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")

user_table_insert = ("INSERT INTO \
                     users (user_id, first_name, last_name,\
                     gender, level) VALUES (%s, %s, %s, %s, %s)\
                     ON CONFLICT (user_id) DO UPDATE \
                     SET level = EXCLUDED.level;")

song_table_insert = ("INSERT INTO \
                     songs (song_id, title, artist_id, year, duration) \
                     VALUES (%s, %s, %s, %s, %s) \
                     ON CONFLICT (song_id) DO NOTHING;")

artist_table_insert = ("INSERT INTO \
                       artists (artist_id, name, location,\
                       lattitude, longitude) VALUES (%s, %s, %s, %s, %s)\
                       ON CONFLICT (artist_id) DO UPDATE \
                       SET location = EXCLUDED.location, \
                       lattitude = EXCLUDED.lattitude, \
                       longitude = EXCLUDED.longitude;")

time_table_insert = ("INSERT INTO \
                     time (start_time, hour, day, week, month, year, weekday)\
                     VALUES (%s, %s, %s, %s, %s, %s, %s)\
                     ON CONFLICT (start_time) DO NOTHING;")

useragent_table_insert = ("INSERT INTO \
                          useragent (user_agent, browser, browser_version,\
                          os, os_version, mobile) \
                          VALUES (%s, %s, %s, %s, %s, %s) \
                          ON CONFLICT (user_agent) DO NOTHING;")

# FIND SONGS

song_select = ("SELECT songs.song_id, artists.artist_id \
               FROM songs \
               JOIN artists ON songs.artist_id = artists.artist_id \
               WHERE songs.title = %s AND artists.name = %s \
               AND songs.duration = %s;")

# ANALYTICS QUERYS

play_location = ("SELECT location, count(location)as total\
                  FROM songplays\
                  GROUP BY(location) \
                  ORDER BY total DESC LIMIT 5;")

play_os_level = ("SELECT songplays.level, useragent.os, COUNT(useragent.os) \
                  FROM songplays JOIN useragent ON\
                  songplays.user_agent = useragent.user_agent\
                  GROUP BY CUBE(level, useragent.os)\
                  ORDER BY (useragent.os);")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create,
                        time_table_create, useragent_table_create]

drop_table_queries = [songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop,
                      time_table_drop, useragent_table_drop]
