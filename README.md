# Tendril Exercise
Software Engineer

## Bokeh charts powered by Django web developement framework

###  Backend: sqlite3, python
__

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

## file structure

```
aws.py
manage.py
mylogger.py
README.md
requirements.txt
start.sh
subset_track_metadata.db
utils.py
songs/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    urls.py
    views.py
    migrations/
        __init__.py
    scripts/
        __init__.py
        aws.py
        common_env.py
        mylogger.py
        part1.py
        plotting.py
    static/
        songs/
            css/
            fonts/
            js/
    templatetags/
        __init__.py
        songs_extras.py
templates/
    songs/
        base_site.html
        home.html
        results.html
tendril_exercise/
    __init__.py
    settings.py
    urls.py
    wsgi.py
```
