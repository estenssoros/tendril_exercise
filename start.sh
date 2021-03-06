#!/bin/bash
SRC_DIR=$(dirname $0)
db="subset_track_metadata.db"
STATIC_DIR="songs/static/songs"
SCRIPTPATH=`pwd -P`
if [[ $1 = "d" ]]; then
  echo '*** running in docker container ***'
  docker run -it \
  -v $SCRIPTPATH:/home/docker/tendril_exercise \
  -e SPOTIPY_CLIENT_ID=$SPOTIPY_CLIENT_ID \
  -e SPOTIPY_CLIENT_SECRET=$SPOTIPY_CLIENT_SECRET \
  -e SPOTIPY_REDIRECT_URI=$SPOTIPY_REDIRECT_URI \
  -p 8000:8000 \
  estenssoros/tendril:1.0
else

  rm -rf $STATIC_DIR
  mkdir -p $STATIC_DIR
  if [ -f $db ]; then
    rm $db
  fi
  wget https://s3.amazonaws.com/sebsbucket/cdn/$db

  sqlite3 $db "ALTER TABLE songs ADD sha256 VARCHAR(64) DEFAULT NULL"
  sqlite3 $db "ALTER TABLE songs ADD u_artist_name VARCHAR(256) DEFAULT NULL"
  sqlite3 $db "ALTER TABLE songs ADD my_songs INT DEFAULT 0"

  pip install -r requirements.txt
  python $SRC_DIR/songs/scripts/part1.py --run

  wget https://github.com/twbs/bootstrap/releases/download/v3.3.7/bootstrap-3.3.7-dist.zip
  unzip -o -d temp bootstrap-3.3.7-dist.zip

  mv temp/bootstrap-3.3.7-dist/css $STATIC_DIR
  mv temp/bootstrap-3.3.7-dist/js $STATIC_DIR
  mv temp/bootstrap-3.3.7-dist/fonts $STATIC_DIR

  rm -rf temp
  rm *.zip

  python manage.py migrate
  python manage.py runserver 0.0.0.0:8000
fi
