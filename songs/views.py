import json
import os

import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import FieldError
from django.db import connections
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from models import Song
from scripts.plotting import Plotter
from scripts.search_spotify import SebSpotipy


def home(request):
    df = pd.read_sql('select * from songs limit 10', con=connections['default'])
    del df['u_artist_name']
    table = df.to_html().replace('dataframe', 'table table-striped')
    fields = []
    with open(os.path.join(settings.BASE_DIR, 'field_explanations.txt')) as f:
        for line in f:
            line = line.strip().split('|')
            fields.append(dict(zip(['name', 'text'], line)))
    context = {'table': table, 'fields': fields}
    return render(request, 'songs/home.html', context)


def create_song_table(artist_name):
    df = song


def results(request):
    cols = ['duration', 'artist_familiarity', 'artist_hotttnesss', 'year']
    df = pd.DataFrame(list(Song.objects.all().values(*cols)))
    for col in cols:
        df[col] = df[col].astype(float)
    desc = df.describe().drop('count').to_html().replace('dataframe', 'table table-hover')
    corr = df.corr().to_html().replace('dataframe', 'table table-hover')

    numeric_fields = ['DecimalField', 'IntegerField']
    fields = [f.name for f in Song._meta.fields if f.get_internal_type() in numeric_fields]

    charts = [
        {"name": "song_count_by_year",
         "backgroundColor": "rgba(255, 99, 132, 0.2)",
         "borderColor": "rgba(255,99,132,1)"},
        {"name": "featured_count_by_year",
         "backgroundColor": "rgba(54, 162, 235, 0.2)",
         "borderColor": "rgba(54, 162, 235, 1)"},
        {"name": "hotttnesss_distribution",
         "backgroundColor": "rgba(255, 206, 86, 0.2)",
         "borderColor": "rgba(255, 206, 86, 1)"},
        {"name": "duration_distribution",
         "backgroundColor": "rgba(75, 192, 192, 0.2)",
         "borderColor": "rgba(75, 192, 192, 1)"},
        {"name": "familiarity_distribution",
         "backgroundColor": "rgba(153, 102, 255, 0.2)",
         "borderColor": "rgba(153, 102, 255, 1)"},
    ]
    context = {'fields': fields,
               'desc': desc,
               'corr': corr,
               'charts': json.dumps(charts)}

    if request.method == 'GET':
        seb_spotipy = SebSpotipy()
        artist_name = request.GET.get('artist_name')
        title = request.GET.get('title')
        context.update(request.GET.dict())

        if not seb_spotipy.connected:
            message = '''
            WARNING: Spotify tokens not present or incorrect.
            Please visit <a href="https://developer.spotify.com/my-applications/#!/applications" targe="_blank">Spotify</a>
            or contact <a href="http://estenssoros.com/" target="_blank">Sebastian Estenssoro</a>
            '''
            messages.warning(request, message)
            context.pop('artist_name', None)
            context.pop('title', None)
            return render(request, 'songs/results.html', context)

        meta_data = None
        cols = ['u_artist_name', 'title', 'duration', 'artist_familiarity', 'artist_hotttnesss', 'year']
        if artist_name:
            songs = list(Song.objects.filter(u_artist_name=artist_name).order_by('title').values(*cols))
            for row in songs:
                row['preview_url'] = seb_spotipy.artist_track(row['u_artist_name'], row['title'])['preview_url']
            meta_data = seb_spotipy.find_artist(artist_name)
            meta_data['songs'] = songs
        if title:
            song = Song.objects.filter(title=title)[0]
            meta_data = seb_spotipy.artist_track(song.artist_name, title)
            meta_data['song'] = song
        context['meta_data'] = meta_data
    return render(request, 'songs/results.html', context)


class ChartAPI(APIView):
    '''
    Returns simple 2d correlation data sets
    '''
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        query_dict = request.GET
        x_axis = query_dict.get('x_axis')
        y_axis = query_dict.get('y_axis')
        try:
            df = pd.DataFrame(list(Song.objects.all().values(x_axis, y_axis)))
        except FieldError:
            return Response('')
        m = df[x_axis] > 0
        n = df[y_axis] > 0
        df = df[m & n]
        scatter = []
        for i, r in df.iterrows():
            scatter.append(dict(zip(['x', 'y'], [r[x_axis], r[y_axis]])))
        data = {'scatter': scatter,
                'title': '{} vs {}'.format(x_axis, y_axis),
                'x_axis': x_axis,
                'y_axis': y_axis}
        return Response(data)


class PlotAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        query_dict = request.GET.dict()
        plotter = Plotter(**query_dict)
        data = plotter.plot()
        return Response(data)


class ArtistAutoCompleteAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        if request.is_ajax():
            q = request.GET.get('term', '')
            query_set = Song.objects.filter(u_artist_name__icontains=q)
            data = sorted(set([x.u_artist_name for x in query_set]))
            return Response(data)


class SongAutoCompleteAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        if request.is_ajax():
            q = request.GET.get('term', '')
            query_set = Song.objects.filter(title__icontains=q)
            data = sorted(set([x.title for x in query_set]))
            return Response(data)
