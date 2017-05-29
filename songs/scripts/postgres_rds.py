import sqlite3
import sys

import psycopg2
from tqdm import tqdm

scon = sqlite3.connect('/Users/sebastian.estenssoro/track_metadata.db')
scurs = scon.cursor()

P_CONN = {'dbname': 'songs',
          'user': 'sebass',
          'host': 'tendrilexercise.cli45ypewqin.us-east-1.rds.amazonaws.com',
          'password': 'seb132435'}

pconn = psycopg2.connect(**P_CONN)
pcurs = pconn.cursor()

scurs.execute('select count(*) from songs')
count = int(scurs.fetchone()[0])
scurs.execute('select * from songs')
cols = [x[0] for x in scurs.description]

sql = 'INSERT INTO track_metadata (%s) ' % ','.join(cols)
wild_cards = '(' + ','.join(['%s'] * len(cols)) + ')'
sql += 'VALUES ' + wild_cards

pcurs.execute('TRUNCATE track_metadata')
LIMIT = 150
queries = []
for row in tqdm(scurs.fetchall(), total=count):
    queries.append(pcurs.mogrify(wild_cards, row))
    if len(queries) == LIMIT:
        pcurs.execute('INSERT INTO track_metadata VALUES' + ','.join(queries))
        pconn.commit()
        queries = []
if queries:
    pcurs.execute('INSERT INTO track_metadata VALUES' + ','.join(queries))
    pconn.commit()
