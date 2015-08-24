# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bump_hunter.models import LogData
from bump_hunter.models import UserInsight, UserInsightForm

import json
import logging
import time
import datetime
import requests
import tweepy
import math
import ibmiotf.application
import uuid
import re

# Authentication Information for @bumps_hunter
## https://twitter.com/bumps_hunter
CONSUMER_KEY        = "QJhFqZOPE9xDRb90ZYUhCaHw2"
CONSUMER_SECRET     = "YErkMoxOmXTmIwqb1QyOO2cP0ZwovXcJeOM9vgcMX7mJKt4MiJ"
ACCESS_TOKEN        = "3315641186-dV9VB8PwJt5eCmyFuFrXrkNNVmYyTVDOXoXmbWx"
ACCESS_TOKEN_SECRET = "Ou9LUOHjfyONE3jtFIoHuuMaqpNlVdzkyeWmmyxDDAgZV"

# Language translation
LT_USERNAME = "c4b210b4-094b-4a9c-b8c3-057c783932d9"
LT_PASSWORD = "VOdojieHmsOw"
LT_URL      = "https://gateway.watsonplatform.net/language-translation/api/v2"

# Twitter insights
TI_USERNAME = "cb0cb3b64354350db2024dfca30e493a"
TI_PASSWORD = "TBOhrFxT4z"
TI_URL      = "https://cb0cb3b64354350db2024dfca30e493a:TBOhrFxT4z@cdeservice.mybluemix.net:443/api/v1"
RED_THRESH = 2.0
# MQTT
ORG_ID = 'g6t2bu'
DEVICE_TYPE = 'MQTTDevice'
DEVICE_ID = 'DQGM50ADF8GJ'
AUTH_TOKEN = ')l3k_j(h(tR4penx3g'

AUTH_METHOD = 'apikey'
API_KEY = 'a-g6t2bu-0lsj9vg8gt'
API_TOKEN = 'YKLe&MtjSvd*FbXYpM'

prev_lat = 0.0
prev_lon = 0.0

# log
logger = logging.getLogger(__name__)

def bump_index(request):
    return render_to_response('bump_hunter/bump_index.html', context_instance=RequestContext(request))

@login_required
def bump_map_roadway(request):
    return render_to_response('bump_hunter/bump_map.html', { 'mode': 'Roadway' }, context_instance=RequestContext(request))

@login_required
def bump_map_sidewalk(request):
    return render_to_response('bump_hunter/bump_map.html', { 'mode': 'Sidewalk' }, context_instance=RequestContext(request))

# twitter insights
@login_required
def bump_map_get_tweets(request):
    # use TI api
    url          = "%s/search" % TI_URL
    headers      = {'Content-type': 'application/json', 'Accept': 'application/json'}
    query = ""
    request_data = { "q": query,
                     "size": 1 }
    response     = requests.get(url, data=json.dumps(request_data), headers=headers, auth=watson_auth_token)

    # update with tranlated string
    if response.status_code == requests.codes.ok:
        LT_result_data = json.loads(response.text)
        LT_str = LT_result_data['translations'][0]['translation']
        update_str = "%s (%s)" % (LT_str, timestamp)
    return JsonResponse({'all_log_data': data_ary, 'markers': markers_ary}, safe=False)

# tweet method
@login_required
def bump_tweet(request):
    # Oauth authenticate
    ## twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    # watson
    watson_auth_token = LT_USERNAME,LT_PASSWORD

    # process str
    status_str = 'Hello. This is the latest infomation of load condition around your area! Check http://bump-hunter.mybluemix.net/bump_hunter'
    timestamp  = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    update_str = "%s (%s)" % (status_str, timestamp)

    # post tweet
    api.update_status(status=update_str)

    # use LT api
    url          = "%s/translate" % LT_URL
    headers      = {'Content-type': 'application/json', 'Accept': 'application/json'}
    request_data = { "model_id": "en-es",
                     "text": status_str }
    response     = requests.post(url, data=json.dumps(request_data), headers=headers, auth=watson_auth_token)

    # update with tranlated string
    if response.status_code == requests.codes.ok:
        LT_result_data = json.loads(response.text)
        LT_str = LT_result_data['translations'][0]['translation']
        update_str = "%s (%s)" % (LT_str, timestamp)
        api.update_status(status=update_str)

    return render_to_response('bump_hunter/bump_map.html',  # 使用するテンプレート
                              context_instance=RequestContext(request))  # その他標準のコンテキスト

@login_required
def bump_map_get_all(request):
    # logger.debug('mode = %s' % request.GET['mode'])
    all_log_data = LogData.objects.filter(log_type__icontains=request.GET['mode'])
    # logger.debug('request = %s' % request)
    data_ary       = []

    for log_data in all_log_data:
        # username = log_data.user.username
        log_dict = {
            'logged_at': log_data.logged_at,
            'lat': float(log_data.lat),
            'lon': float(log_data.lon),
            'acc': float(log_data.acc),
            # 'username': username,
        }

        data_ary.append(log_dict)

    return JsonResponse({'all_log_data': data_ary, }, safe=False)

@login_required
def bump_sensing_roadway(request):
    do_subscribe('Roadway')
    return render_to_response('bump_hunter/bump_sensing.html', { 'mode': 'Roadway' }, context_instance=RequestContext(request))

@login_required
def bump_sensing_sidewalk(request):
    do_subscribe('Sidewalk')
    return render_to_response('bump_hunter/bump_sensing.html', { 'mode': 'Sidewalk' }, context_instance=RequestContext(request))

# for saving data from mqtt connection
def do_subscribe(mode):
    mqtt_options = {
        'org': ORG_ID,
        'id': str(uuid.uuid4()),
        'auth-method': AUTH_METHOD,
        'auth-key': API_KEY,
        'auth-token': API_TOKEN,
    }

    # prev_lat = 0
    # prev_lon = 0

    def myEventCallback(event):
        global prev_lat, prev_lon

        log = event.data
        logger.debug('log = %s' % log)

        logger.debug('prev_lat = %f' % prev_lat)
        logger.debug('prev_lon = %f' % prev_lon)

        if not (prev_lat == log['lat'] and prev_lon == log['lon']):
            prev_lat = log['lat']
            prev_lon = log['lon']

            user = User.objects.get(pk=log['user_id'])
            logger.debug('user = %s' % user)
            logged_at = datetime.datetime.fromtimestamp(log['logged_at'])

            log_data = LogData(
                lat=log['lat'],
                lon=log['lon'],
                acc=log['acc'],
                log_type=mode,
                logged_at=logged_at,
                user=user,
            )
            logger.debug('log_data = %s' % log_data)

            log_data.save()

    try:
        client = ibmiotf.application.Client(mqtt_options)
        client.connect()
        client.deviceEventCallback = myEventCallback
        client.subscribeToDeviceEvents(DEVICE_TYPE, DEVICE_ID, "+")
    except ibmiotf.ConnectionException as e:
        logger.error('Connection failed: %s' % e)

@login_required
def bump_chart(request):
    return render_to_response('bump_hunter/bump_chart.html', context_instance=RequestContext(request));

@login_required
def bump_insights(request, id=None):
    user_name = request.user.username

    if request.method == "GET" and len(request.GET) > 0:
        # logger.debug('GET = %s' % request.GET)
        lat = request.GET['lat'] if (len(request.GET['lat']) > 0) else None
        lon = request.GET['lon'] if (len(request.GET['lon']) > 0) else None
        mode = request.GET['mode'] if (len(request.GET['mode']) > 0) else "Roadway"
        form = UserInsightForm(initial={'user_name': user_name, 'lat': lat, 'lon': lon, 'insight_type': mode.lower()})
    else:
        form = UserInsightForm(initial={'user_name': user_name})

    hidden_keyword = ""

    if request.method == "POST":
        if id is not None:
            instance = get_object_or_404(UserInsight, id=id)
        else:
            form         = UserInsightForm(request.POST)
            if form.is_valid():
                user_insight = form.save(commit=False)
                hidden_keyword = user_insight.location
                user_insight.save()
                logger.debug('user_insight.insight_type = %s' % user_insight.insight_type)
                return redirect('/bump_hunter/bump_map/' + user_insight.insight_type + '/')
            else:
                print form.errors

    return render_to_response('bump_hunter/bump_insights.html', {'form':form, 'hidden_keyword': hidden_keyword}, context_instance=RequestContext(request))

@login_required
def bump_insights_get_all(request):
    if len(request.GET) > 0:
        all_insight_data = UserInsight.objects.filter(insight_type__icontains=request.GET['mode'])
    else:
        all_insight_data = UserInsight.objects.all()

    data_ary = []
    for cur_data in all_insight_data:
        insight_dict = {
            'lat': float(cur_data.lat),
            'lon': float(cur_data.lon),
            'user_name': cur_data.user_name,
            'insight_type': cur_data.insight_type,
            'location_name': cur_data.location,
            'comment': cur_data.comment,
            'created_at': cur_data.created_at
        }
        data_ary.append(insight_dict)
    return JsonResponse({'all_insight_data': data_ary}, safe=False)

def bump_insights_get_tweets(request):
    # use searched query
    query = request.GET['query'] if (len(request.GET['query']) > 0) else "Tokyo Station"
    # use TI api
    url            = "%s/messages/search" % TI_URL
    headers        = {'Content-type': 'application/json', 'Accept': 'application/json'}
    positive_query = "%s sentiment: positive" % query
    negative_query = "%s sentiment: negative" % query
    tweets_size    = 3
    reg_format     = re.compile("(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})")

    # requests
    positive_response = requests.get(url, params={"q": positive_query, "size": tweets_size}, headers=headers)
    negative_response = requests.get(url, params={"q": negative_query, "size": tweets_size}, headers=headers)

    p_tweets = []
    n_tweets = []
    if positive_response.status_code == requests.codes.ok:
        positive_text = json.loads(positive_response.text)
        for p_data in positive_text['tweets']:
            if p_data.has_key('message'):
                target_data = p_data['message']
                date_reg    = reg_format.search(target_data['postedTime'])
                tweet_data  = {'user_name': target_data['actor']['displayName'],
                               'at_name': target_data['actor']['preferredUsername'],
                               'img_url':  target_data['actor']['image'],
                               'body_text': target_data['body'],
                               'posted_at': "%s %s" % (date_reg.group(1), date_reg.group(2))
                           }
                p_tweets.append(tweet_data)
        p_tweets.reverse()
    if negative_response.status_code == requests.codes.ok:
        negative_text = json.loads(negative_response.text)
        for n_data in negative_text['tweets']:
            if n_data.has_key('message'):
                target_data = n_data['message']
                date_reg    = reg_format.search(target_data['postedTime'])
                tweet_data  = {'user_name': target_data['actor']['displayName'],
                               'at_name': target_data['actor']['preferredUsername'],
                               'img_url':  target_data['actor']['image'],
                               'body_text': target_data['body'],
                               'posted_at': "%s %s" % (date_reg.group(1), date_reg.group(2))
                           }
                n_tweets.append(tweet_data)
        n_tweets.reverse()
    return JsonResponse({'positive_tweets': p_tweets, 'negative_tweets': n_tweets}, safe=False)

def logout(request):
    logout(request)
    render_to_response('bump_hunter/logout.html', context_instance=RequestContext(request))
