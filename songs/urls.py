from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^results/(?P<chart_type>[\w-]+)/$', views.results),
    url(r'^results/$', views.results),
    ]
