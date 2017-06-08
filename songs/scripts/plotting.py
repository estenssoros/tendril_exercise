import os

import numpy as np
import pandas as pd
from django.conf import settings
from django.db import connections
from tqdm import tqdm

import common_env
from aws import connect_s3


def ensure_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def make_title(s):
    s = [x.title() for x in s.split('_')]
    return ' '.join(s)


def bins_to_list(bins):
    bins = list(bins)
    tuples = [x[1:-1].split(', ') for x in bins]
    labels = []
    for t in tuples:
        labels.append(t[0])
        labels.append(t[1])
    return labels


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


class Plotter(object):
    def __init__(self, chart_type, artist_name=None, title=None):
        self.plot = getattr(self, chart_type)
        self.artist_name = html_decode(artist_name) if artist_name else None
        self.title = html_decode(title) if title else None
        self.data = {'title': make_title(chart_type)}
        self.num_bins = 50

    def _sql_pandas(self, sql):
        return pd.read_sql(sql, con=connections['default'])

    def _remove_outliers(self, df, col):
        return df[np.abs(df[col] - df[col].mean()) <= (3 * df[col].std())]

    def hotttnesss_distribution(self):
        return self._create_histogram('artist_hotttnesss', remove_outliers=False, rounding=2)

    def familiarity_distribution(self):
        return self._create_histogram('artist_familiarity', remove_outliers=True, rounding=2)

    def duration_distribution(self):
        return self._create_histogram('duration', remove_outliers=True, rounding=0)

    def _create_histogram(self, col, remove_outliers=False, rounding=0):
        df = self._sql_pandas('select %s from songs' % col)
        if remove_outliers:
            df = self._remove_outliers(df, col)
        count1, labels = np.histogram(df[col], bins=self.num_bins)
        bins = [round(x, rounding) for x in labels]
        self.data['labels'] = bins
        self.data['ds1'] = {'values': count1.tolist()}
        if self.artist_name or self.title:
            if self.artist_name:
                df = self._sql_pandas('select %s from songs where u_artist_name = "%s"' % (col, self.artist_name))
            if self.title:
                df = self._sql_pandas('select %s from songs where title = "%s"' % (col, self.title))
            count2, _ = np.histogram(df[col], bins=bins)
            count2[count2 > 0] = count1[count2 > 0]
            data = {'values': count2.tolist()}
            self.data['ds2'] = data
        return self.data

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
        self.data['labels'] = df['year']
        self.data['ds1'] = {'values': list(df['cnt'])}
        if self.artist_name or self.title:
            if self.artist_name:
                sql = '''
                SELECT year
                    , count(*) as cnt
                FROM songs
                WHERE u_artist_name = "%s"
                GROUP BY year
                '''
                new_df = self._sql_pandas(sql % self.artist_name)
            if self.title:
                sql = '''
                SELECT year
                    , count(*) as cnt
                FROM songs
                WHERE title = "%s"
                GROUP BY year
                '''
                new_df = self._sql_pandas(sql % self.title)
            ds2 = pd.merge(df, new_df, how='left', on='year').fillna(0)
            data = {'values': list(ds2['cnt_y'])}
            self.data['ds2'] = data
        return self.data

    def featured_count_by_year(self):
        '''
        Songs with featured artists by year
        '''
        sql = '''
        SELECT artist_name
            , year
            , u_artist_name
        FROM songs
        WHERE year > 0
        '''
        df = self._sql_pandas(sql)
        u_names = pd.unique(df['u_artist_name']).tolist()
        df = df[['year']][~df['artist_name'].isin(u_names)]
        gb = df.groupby('year').size().reset_index()
        self.data['labels'] = gb['year'].values.tolist()
        self.data['ds1'] = {'values': gb[0].values.tolist()}
        if self.artist_name or self.title:
            if self.artist_name:
                sql = '''
                SELECT artist_name
                    , year
                    , u_artist_name
                FROM songs
                WHERE u_artist_name = "%s"
                '''
                new_df = self._sql_pandas(sql % self.artist_name)
            if self.title:
                sql = '''
                SELECT artist_name
                    , year
                    , u_artist_name
                FROM songs
                WHERE title = "%s"
                '''
                new_df = self._sql_pandas(sql % self.title)
            new_df = new_df[new_df['artist_name'] != new_df['u_artist_name']]
            new_gb = new_df.groupby('year').size().reset_index()
            ds2 = pd.merge(gb, new_gb, how='left', on='year').fillna(0)
            data = {'values': ds2['0_y']}
            self.data['ds2'] = data
        return self.data


def save_image(self, img_data, title):
    '''
    save png image to aws
    '''
    save_name = to_snake(title) + '.png'
    path = os.path.join(directory, save_name)
    key = bucket.new_key(path)
    key.set_contents_from_file(img_data, policy='public-read')


def plot_scatter(df):
    '''
    import io
    import matplotlib.pyplot as plt
    from pandas import scatter_matrix
    '''
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
    pass
