# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from bump_hunter import views
urlpatterns = patterns('',
                       url(r'^bump_map/$', views.bump_map, name='bump_map'),
                   )
