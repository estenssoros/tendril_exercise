# coding: utf-8
import hashlib
import os
import sqlite3
import sys
import time

import pandas as pd
from django.conf import settings
from tqdm import tqdm

import common_env


class Songs(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        self.df = self.get_df()

    def hasher(self, s):
        hash_obj = hashlib.sha256(s.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_df(self):
        df = pd.read_sql('select * from songs', con=self.conn)
        df['sha256'] = df.apply(lambda x: self.hasher(x['artist_name']), axis=1)
        return df

    def update_table(self):
        # 1.44s user 0.14s system 99% cpu 1.596 total
        sql = '''UPDATE songs SET sha256 = ? WHERE track_id = ?'''
        count = 1
        for i, r in tqdm(self.df.iterrows(), total=len(self.df), desc='syncing sqlite3'):
            row = (r['sha256'], r['track_id'])
            self.curs.execute(sql, row)
            count += 1
            if count % 100 == 0:
                self.conn.commit()
        self.conn.commit()

    def shutdown(self):
        self.curs.close()
        self.conn.close()

    def run(self):
        self.update_table()


def main():
    db_path = os.path.join(settings.BASE_DIR,'subset_track_metadata.db')
    songs = Songs(db_path)
    songs.run()
    songs.shutdown()


if __name__ == '__main__':
    main()
