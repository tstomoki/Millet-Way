# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
## gmapi
import simplejson as json
from gmapi import maps
from gmapi.forms.widgets import GoogleMap

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':900, 'height':700}))

def bump_map(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(35.90061,139.933694),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 13,
        'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    marker = maps.Marker(opts = {
        'map': gmap,
        'position': maps.LatLng(35.90061,139.933694),
    })
    maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
    maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
    info = maps.InfoWindow({
        'content': 'Hello!',
        'disableAutoPan': True
    })
    info.open(gmap, marker)
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('bump_hunter/bump_map.html', context)
