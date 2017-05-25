import pandas as pd
from bokeh.embed import components
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.db import connections

import common_env


def sql_pandas(sql):
    return pd.read_sql(sql, con=connections['default'])


def familiarity_v_hotness():
    df = sql_pandas('select artist_familiarity, artist_hotttnesss, year from songs')
    df = df[df['artist_hotttnesss'] > 0]
    plot = figure()
    plot.xaxis.axis_label = 'familiarity'
    plot.yaxis.axis_label = 'hotttnesss'
    plot.circle(df['artist_familiarity'], df['artist_hotttnesss'], fill_alpha=0.2, size=8)
    return components(plot, CDN)


def hotness_v_duration():
    df = sql_pandas('select duration, artist_hotttnesss, year from songs')
    df = df[df['artist_hotttnesss'] > 0]
    plot = figure()
    plot.xaxis.axis_label = 'duration'
    plot.yaxis.axis_label = 'hotttnesss'
    plot.circle(df['duration'], df['artist_hotttnesss'], fill_alpha=0.2, size=8, color='red')
    return components(plot, CDN)
