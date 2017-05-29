DROP TABLE IF EXISTS track_metadata;
CREATE TABLE track_metadata (
  track_id VARCHAR(18)
  , title VARCHAR(255)
  , song_id VARCHAR(18)
  , release VARCHAR(188)
  , artist_id VARCHAR(18)
  , artist_mbid VARCHAR(36)
  , artist_name VARCHAR(373)
  , duration DECIMAL(10,6)
  , artist_familiarity DECIMAL(7,6)
  , artist_hotttnesss DECIMAL(7,6)
  , year INT
  , track_7digitalid INT
  , shs_perf INT
  , shs_work INT
  , PRIMARY KEY (track_id)
)
;
