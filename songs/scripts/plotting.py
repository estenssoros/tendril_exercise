import pandas as pd
from bokeh.charts import HeatMap, Histogram, bins
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.db import connections
from tqdm import tqdm

import common_env


class Plotter(object):
    def __init__(self):
        pass

    def _sql_pandas(self, sql):
        return pd.read_sql(sql, con=connections['default'])

    def familiarity_v_hotness(self):
        df = self._sql_pandas('select artist_familiarity, artist_hotttnesss, year from songs')
        df = df[df['artist_hotttnesss'] > 0]
        plot = figure()
        plot.xaxis.axis_label = 'familiarity'
        plot.yaxis.axis_label = 'hotttnesss'
        plot.scatter(df['artist_familiarity'], df['artist_hotttnesss'], size=3, color="#3A5785", alpha=0.6)
        return components(plot, CDN)

    def hotness_v_duration(self):
        df = self._sql_pandas('select duration, artist_hotttnesss, year from songs')
        df = df[df['artist_hotttnesss'] > 0]
        plot = figure()
        plot.xaxis.axis_label = 'duration'
        plot.yaxis.axis_label = 'hotttnesss'
        plot.scatter(df['duration'], df['artist_hotttnesss'], size=3, color="#3A5785", alpha=0.6)
        return components(plot, CDN)

    def heatmap(self):
        df = self._sql_pandas('select artist_familiarity, duration, artist_hotttnesss, year from songs')
        df = df[df['year'] > 0]
        hm = HeatMap(df, x='year', y=bins('duration'), values='artist_hotttnesss', title='artist_hotttnesss')
        return components(hm, CDN)

    def song_count_by_year(self):
        sql = '''
        SELECT year
        FROM songs
        WHERE year > 0
        '''
        df = self._sql_pandas(sql)
        years = pd.unique(df['year'])
        hist = Histogram(df, values='year', bins=len(years))
        return components(hist, CDN)

    def featured_by_year(self):
        sql = '''
        SELECT artist_name,year
        FROM songs
        WHERE year > 0
        '''
        df = self._sql_pandas(sql)
        df = df[['year']][df['artist_name'].str.contains('feat.')]
        years = pd.unique(df['year'])
        hist = Histogram(df, values='year', bins=len(years))
        return components(hist, CDN)


# TODO featured artists over time along with hotttnesss

if __name__ == '__main__':
    pd.set_option('display.max_rows', 300)
    pd.set_option('display.max_columns', 10)
    pd.set_option('display.width', 1000)
    sql = '''SELECT * FROM songs'''
    df = pd.read_sql(sql, con=connections['default'])
