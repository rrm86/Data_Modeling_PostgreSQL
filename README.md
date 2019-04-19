
# Dimensional Data Model with PostgreSQL

### Summary

This project aims to build a data model that makes possible a music streaming app 
understands the user's activities and behavior.
 

The data model must have fast responses, be easy to understand and trustworthy. 
In order to reach these aims, this project read and transforms the original data 
using python and implements a Star Schema approach using PostgreSQL.


![star_schema](https://imgur.com/a/ns2LDVW)


## Original Data

The original dataset is composite for two different kinds of files:

 - Song Dataset
 - Log Dataset

### Song Dataset
The song dataset  is in JSON format and contains metadata 
about a song and the artist of that song. 

Below you can see an example of how song file looks like:
```ssh
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```
### Log Dataset
The second dataset consists of log files in JSON format. 
The log file contains the activity logs from a music streaming app.

## Data Model

### Data Cleansing
Before to insert data in tables, is important to make sure about data quality. 
This project uses the pandas library to check missing values and convert data types when necessary.

### Fact Table

#### songplays : records in log data associated with song plays

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

#### users : users in the app

user_id, first_name, last_name, gender, level

#### songs : songs in music database

song_id, title, artist_id, year, duration

#### artists : artists in music database

artist_id, name, location, lattitude, longitude

#### time : timestamps of records in songplays broken down into specific units

start_time, hour, day, week, month, year, weekday

#### useragent : User's Devices broken into specific units 

user_agent, browser, browser_version, os, os_version, mobile

## Code

### Command Line Application

#### Create/drop tables create_tables.py
```ssh
$ python create_tables.py
```
#### ETL - read files from data directory, transform and insert into tables

```ssh
$ python etl.py
```
### Viewing the Jyputer Notebook

#### In order to use .ipynb files you can run:

```ssh
$ jupyter notebook
```

#### test.ipynb - Contain test querys

#### etl.ipynb - Exploratory ETL 

#### analytics.ipynb - Example of analytics querys and plots

## Prerequisites

The Code is written in Python 3.6.3 . If you don't have Python installed you can find it [here]. 
If you are using a lower version of Python you can upgrade using the pip package, 
ensuring you have the latest version of pip.

To install pip run in the command Line:
```sh
$ python -m ensurepip -- default-pip
```
To upgrade pip:
```sh
$ python -m pip install -- upgrade pip setuptools wheel
```
To upgrade Python:
```ssh
$ pip install python -- upgrade
```
Additional Packages that are required are: Jupyter, Psycopg2, Pandas, User_agents, and Bokeh.

You can donwload them using pip

Jupyter:
```ssh
$ pip install jupyter
```
Psycopg2:
```ssh
$ pip install psycopg2
```
Pandas:
```ssh
$ pip install pandas
```
User_agents:
```ssh
$ pip install install pyyaml ua-parser user-agents
```
Bokeh:
```ssh
$ pip install bokeh
```

[//]: #

   [here]: <https://www.python.org/downloads/>