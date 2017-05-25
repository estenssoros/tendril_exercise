from django.http import HttpResponse
from django.shortcuts import render

from scripts.plotting import Plotter


def home(request):
    return render(request, 'songs/home.html')


def results(request, chart_type=None):
    plotter = Plotter()
    options = [x for x in dir(plotter) if not x.startswith('_')]
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
    context = {'options': options,
               'title': chart_type,
               'the_script': script,
               'the_div': div}
    return render(request, 'songs/results.html', context)
