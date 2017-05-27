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


## limitiations
Sqlite doesn't support multi-insert-update statements or update-join statements. Data must be updated iteratively
