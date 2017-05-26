import io
import os

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from bokeh.charts import HeatMap, Histogram, bins
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.conf import settings
from django.db import connections
from pandas.tools.plotting import scatter_matrix
from tqdm import tqdm

import common_env
from aws import connect_s3

matplotlib.use('Agg')


def ensure_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Plotter(object):
    def __init__(self):
        pass

    def _sql_pandas(self, sql):
        return pd.read_sql(sql, con=connections['default'])

    def heatmap(self):
        '''
        Hotness as impacted by year and duration of song
        '''
        df = self._sql_pandas('select artist_familiarity, duration, artist_hotttnesss, year from songs')
        df = df[df['year'] > 0]
        hm = HeatMap(df, x='year', y=bins('duration'), values='artist_hotttnesss')
        return components(hm, CDN)

    def song_count_by_year(self):
        '''
        The count of songs by year
        '''
        sql = '''
        SELECT year
            ,count(*) as cnt
        FROM songs
        WHERE year > 0
        GROUP BY year
        '''
        df = self._sql_pandas(sql)
        data = {'labels': df['year'].values.tolist(),
                'values': df['cnt'].values.tolist()}
        return data

    def featured_count_by_year(self):
        '''
        Songs with featured artists by year
        '''
        sql = '''
        SELECT artist_name
            ,year
        FROM songs
        WHERE year > 0
        '''
        df = self._sql_pandas(sql)
        df = df[['year']][df['artist_name'].str.contains('feat.')]
        gb = df.groupby('year').size().reset_index()
        data = {'labels': gb['year'].values.tolist(),
                'values': gb[0].values.tolist()}
        return data


def save_image(self, img_data, title):
    save_name = to_snake(title) + '.png'
    path = os.path.join(directory, save_name)
    key = bucket.new_key(path)
    key.set_contents_from_file(img_data, policy='public-read')


def plot_scatter(df):
    for col in df.columns:
        df[col] = df[col].astype(float)
    axs = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    n = len(df.columns)
    for x in range(n):
        for y in range(n):
            ax = axs[x, y]
            ax.xaxis.label.set_rotation(90)
            ax.yaxis.label.set_rotation(0)
            ax.yaxis.labelpad = 50
    plt.tight_layout()

    S3_SITE = 'http://s3.amazonaws.com/tendril'
    save_name = 'scatter_matrix.png'

    aws = False
    try:
        bucket = connect_s3()
        aws = True
        directory = 'tendril/images'
    except KeyError:
        directory = os.path.join(settings.BASE_DIR, 'songs/static/songs/images')
        ensure_exists(directory)

    path = os.path.join(directory, save_name)
    if aws:
        img_data = io.BytesIO()
        plt.savefig(img_data, dpi=250)
        img_data.seek(0)
        key = bucket.new_key(path)
        key.set_contents_from_file(img_data, policy='public-read')
    else:
        plt.savefig(path, dpi=250)
    plt.close()


if __name__ == '__main__':
    pd.set_option('display.max_rows', 300)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    sql = '''SELECT * FROM songs'''
    df = pd.read_sql(sql, con=connections['default'])
