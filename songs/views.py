import os

import pandas as pd
from django.conf import settings
from django.core.exceptions import FieldError
from django.db import connections
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from models import Song
from scripts.plotting import Plotter
from serializers import SongSerializer


def home(request):
    df = pd.read_sql('select * from songs limit 10', con=connections['default'])
    del df['u_artist_name']
    table = df.to_html().replace('dataframe', 'table table-hover')
    fields = []
    with open(os.path.join(settings.BASE_DIR, 'field_explanations.txt')) as f:
        for line in f:
            line = line.strip().split('|')
            fields.append(dict(zip(['name', 'text'], line)))
    context = {'table': table, 'fields': fields}
    return render(request, 'songs/home.html', context)


def results(request, chart_type=None):
    cols = ['duration', 'artist_familiarity', 'artist_hotttnesss', 'year']
    df = pd.DataFrame(list(Song.objects.all().values(*cols)))
    for col in cols:
        df[col] = df[col].astype(float)
    desc = df.describe().drop('count').to_html().replace('dataframe', 'table table-hover')
    corr = df.corr().to_html().replace('dataframe', 'table table-hover')

    numeric_fields = ['DecimalField', 'IntegerField']
    fields = [f.name for f in Song._meta.fields if f.get_internal_type() in numeric_fields]
    context = {'fields': fields,
               'desc': desc,
               'corr': corr, }
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


def make_title(s):
    s = [x.title() for x in s.split('_')]
    return ' '.join(s)


class PlotAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        plotter = Plotter()
        query_dict = request.GET
        chart_type = query_dict.get('chart_type')
        func = getattr(plotter, chart_type)
        data = func()
        data['title'] = make_title(chart_type)
        return Response(data)


class ArtistAutoCompleteAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        if request.is_ajax():
            q = request.GET.get('term', '')
            query_set = Song.objects.filter(artist_name__icontains=q)
            data = sorted(set([x.artist_name for x in query_set]))
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

# def results(request, chart_type=None):
#     cols = ['duration', 'artist_familiarity', 'artist_hotttnesss', 'year']
#     df = pd.DataFrame(list(Song.objects.all().values(*cols)))
#     for col in cols:
#         df[col] = df[col].astype(float)
#     desc = df.describe().drop('count').to_html().replace('dataframe', 'table table-hover')
#     corr = df.corr().to_html().replace('dataframe', 'table table-hover')
#
#     plotter = Plotter()
#     options = sorted([x for x in dir(plotter) if not x.startswith('_')])
#     if chart_type == None:
#         chart_type = 'familiarity_v_hotness'
#         plotter = getattr(plotter, chart_type)
#     else:
#         try:
#             plotter = getattr(plotter, chart_type)
#         except AttributeError:
#             chart_type = 'familiarity_v_hotness'
#             plotter = getattr(plotter, chart_type)
#
#     script, div = plotter()
#     context = {'desc': desc,
#                'corr': corr,
#                'options': options,
#                'title': chart_type,
#                'the_script': script,
#                'the_div': div,
#                'doc': plotter.__doc__}
#     return render(request, 'songs/results.html', context)
