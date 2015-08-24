# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, static
import django.contrib.auth.views
from bump_hunter import views
from django.http import HttpResponseRedirect
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', lambda r: HttpResponseRedirect('bump_index/')),
    (r'^bump_map/$', lambda r: HttpResponseRedirect('/bump_hunter/bump_index/')),
    (r'^bump_sensing/$', lambda r: HttpResponseRedirect('/bump_hunter/bump_index/')),
    url(r'^bump_index/$', views.bump_index, name='bump_index'),
    url(r'^bump_map/roadway/$', views.bump_map_roadway, name='bump_map_roadway'),
    url(r'^bump_map/sidewalk/$', views.bump_map_sidewalk, name='bump_map_sidewalk'),
    url(r'^bump_tweet/$', views.bump_tweet, name='bump_tweet'),
    url(r'^bump_map/get_all/$', views.bump_map_get_all, name='bump_map_get_all'),
    url(r'^bump_map/get_tweets/$', views.bump_map_get_tweets, name='bump_map_get_tweets'),
    url(r'^bump_sensing/roadway/$', views.bump_sensing_roadway, name='bump_sensing_roadway'),
    url(r'^bump_sensing/sidewalk/$', views.bump_sensing_sidewalk, name='bump_sensing_sidewalk'),
    url(r'^bump_chart/$', views.bump_chart, name='bump_chart'),
    url(r'^bump_insights/$', views.bump_insights, name='bump_insights'),
    url(r'^bump_insights/get_all/$', views.bump_insights_get_all, name='bump_insights_get_all'),
    url(r'^bump_insights/get_tweets/$', views.bump_insights_get_tweets, name='bump_insights_get_tweets'),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'bump_hunter/login.html'}),
    url(r'^logout/$', django.contrib.auth.views.logout, {'template_name': 'bump_hunter/logout.html'}),
)
