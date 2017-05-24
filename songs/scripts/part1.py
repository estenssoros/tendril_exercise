# coding: utf-8
import hashlib
import os
import sqlite3
import sys
import time
from argparse import ArgumentParser

import pandas as pd
from django.conf import settings
from tqdm import tqdm

import common_env
import mylogger

parser = ArgumentParser(description='validate sqoop commands by comparing mysql to hadoop')
parser.add_argument('--run', action="store_true")
parser.add_argument('--test', action="store_true")
args = parser.parse_args()


class Songs(object):
    '''
    Connects to sqlite3 database and create sha256 column
    '''

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.curs = self.conn.cursor()
        self.logger = mylogger.mylogger()
        self.df = self.get_df()

    def hasher(self, s):
        hash_obj = hashlib.sha256(s.encode('utf-8'))
        return hash_obj.hexdigest()

    def get_df(self):
        self.logger.info('reading data from sqlite3')
        df = pd.read_sql('select track_id, artist_name from songs', con=self.conn)
        self.logger.info('converting artist name to sha256')
        df['sha256'] = df.apply(lambda x: self.hasher(x['artist_name']), axis=1)
        return df

    def update_table(self):
        self.logger.info('updating table')
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
        self.shutdown()


def main():
    songs = Songs(settings.DATABASES['default']['NAME'])
    if args.run:
        songs.run()
    elif args.test:
        pass


if __name__ == '__main__':
    main()
