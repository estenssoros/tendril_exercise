import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from models import Song
from scripts.plotting import Plotter


def home(request):
    return render(request, 'songs/home.html')


def results(request, chart_type=None):
    cols = ['duration', 'artist_familiarity', 'artist_hotttnesss', 'year']
    df = pd.DataFrame(list(Song.objects.all().values(*cols)))
    for col in cols:
        df[col] = df[col].astype(float)
    desc = df.describe().drop('count').to_html().replace('dataframe', 'table table-hover')
    corr = df.corr().to_html().replace('dataframe', 'table table-hover')

    plotter = Plotter()
    options = sorted([x for x in dir(plotter) if not x.startswith('_')])
    if chart_type == None:
        chart_type = 'familiarity_v_hotness'
        plotter = getattr(plotter, chart_type)
    else:
        try:
            plotter = getattr(plotter, chart_type)
        except AttributeError:
            chart_type = 'familiarity_v_hotness'
            plotter = getattr(plotter, chart_type)

    script, div = plotter()
    context = {'desc': desc,
               'corr': corr,
               'options': options,
               'title': chart_type,
               'the_script': script,
               'the_div': div,
               'doc': plotter.__doc__}
    return render(request, 'songs/results.html', context)
