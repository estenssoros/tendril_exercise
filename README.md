# Tendril Exercise
Software Engineer

## Chart.js powered by Django web developement framework

- Ajax calls to Django Rest Framework
- Backend: sqlite3, python

## Getting Started

Do you have docker?

Yes!
```
$ ./start.sh d (the d is for "docker")
```


No...
```
make sure you have wget installed
$ apt-get wget
$ brew install wget
$ ./start.sh
```
- download subset_track_metadada.db
- add fields to database
- download v3.3.7 twitter bootstrap to static directory
- pip install requirements.txt
- migrate django admin tables to database
- start webserver

## Spotify
get [credentials] (https://developer.spotify.com/my-applications/#!/applications)

set your environment variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

or you can just use mine...

## limitiations
Sqlite doesn't support multi-insert-update statements or update-join statements. Data must be updated iteratively


## Postgres Notes
```
select * from pg_stat_activity;
select pg_cancel_backend(<pid of the process>);
expanded view: \x
show tables: \dt
use [dbname]: \c[dbname]
```
secret sauce:
```
args_str = ','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in tup)
cur.execute("INSERT INTO table VALUES " + args_str)
```
