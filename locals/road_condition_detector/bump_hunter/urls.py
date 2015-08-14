# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import django.contrib.auth.views
from bump_hunter import views

urlpatterns = patterns('',
    url(r'^bump_map/$', views.bump_map, name='bump_map'),
    url(r'^bump_sensing/$', views.bump_sensing, name='bump_sensing'),
    url(r'^login/', django.contrib.auth.views.login, {'template_name': 'bump_hunter/login.html'}),
)
