from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^results/(?P<chart_type>[\w-]+)/$', views.results),
    url(r'^results/$', views.results),
    url(r'^api/chart/$', views.ChartAPI.as_view()),
    url(r'^api/plot_api/$', views.PlotAPI.as_view()),
    url(r'^api/artist_autocomplete/$', views.ArtistAutoCompleteAPI.as_view()),
    url(r'^api/song_autocomplete/$', views.SongAutoCompleteAPI.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
