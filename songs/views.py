from django.http import HttpResponse
from django.shortcuts import render

from scripts.plotting import familiarity_v_hotness, hotness_v_duration


def home(request):
    return render(request, 'songs/home.html')


def results(request, chart_type=None):
    plotters = {'familiarity_v_hotness': familiarity_v_hotness,
                'hotness_v_duration': hotness_v_duration}
    if chart_type == None:
        plotter = familiarity_v_hotness
    else:
        plotter = plotters[chart_type]

    script, div = plotter()
    context = {'title': chart_type, "the_script": script, "the_div": div}
    return render(request, 'songs/results.html', context)
