# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bump_hunter.models import LogData

import json
import logging
import time
import datetime
import requests
import tweepy
import math

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
TI_URL      = "https://cb0cb3b64354350db2024dfca30e493a:TBOhrFxT4z@cdeservice.mybluemix.net"

logger = logging.getLogger(__name__)

@login_required
def bump_map(request):
    return render_to_response('bump_hunter/bump_map.html',  # 使用するテンプレート
                              context_instance=RequestContext(request))  # その他標準のコンテキスト

# twitter insights
@login_required
def twitter_insights(request):
    return render_to_response('bump_hunter/twitter_insights.html',  # 使用するテンプレート
                              context_instance=RequestContext(request))  # その他標準のコンテキスト    

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

    # process str [WIP]
    status_str = 'Hello'
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
    all_log_data = LogData.objects.all()
    # logger.debug('all_log_data = %s' % all_log_data)
    data_ary = []
    cur = 0
    next = 1
    while cur < len(all_log_data) - 1:
        cur_data = all_log_data[cur]
        cur_lat = float(cur_data.lat)
        cur_lon = float(cur_data.lon)
        log_dict = {
            'logged_at': cur_data.logged_at,
            'lat': cur_lat,
            'lon': cur_lon,
        }
        acc_sum = cur_data.get_acc_size()

        count = 1
        next_data = all_log_data[cur + count]
        next_lat = float(next_data.lat)
        next_lon = float(next_data.lon)
        while cur + count < len(all_log_data) - 1 and cur_lat == next_lat and cur_lon == next_lon:
            acc_sum += next_data.get_acc_size()
            count += 1
            next_data = all_log_data[cur + count]
            next_lat = float(next_data.lat)
            next_lon = float(next_data.lon)

        cur += count + 1
        log_dict['acc'] = acc_sum / count
        data_ary.append(log_dict)

    # for log_data in all_log_data:
    #     log_dict = {}
    #     log_dict['lat'] = float(log_data.lat)
    #     log_dict['lon'] = float(log_data.lon)
    #     log_dict['logged_at'] = log_data.logged_at
    #     log_dict['acc'] = math.sqrt(math.pow(log_data.acc_x, 2) + math.sqrt(log_data.acc_y, 2) + math.pow(log_data.acc_z, 2))
    #     # log_dict['user'] = unicode(log_data.user)
    #     # logger.debug('log_data.user = %s' % log_data.user)
    #     data_ary.append(log_dict)

    return JsonResponse({'all_log_data': data_ary}, safe=False)

@login_required
def bump_sensing(request):
    return render_to_response('bump_hunter/bump_sensing.html', context_instance=RequestContext(request));

@login_required
def bump_sensing_register(request):
    # logger.debug('POST = %s' % request.POST)
    logs = json.loads(request.POST['log_json_str'])['logs']
    logger.debug('logs = %s' % logs)

    if logs is not None:
        user = User.objects.get(username=request.user)
        logger.debug('user = %s' % user)

        for count, log in enumerate(logs, start=1):
            logger.debug('#%d log = %s' % (count, log))
            logged_at = datetime.datetime.fromtimestamp(log['logged_at'])
            # logger.debug('logged_at = %s' % logged_at)
            log_data = LogData(
                lat=log['lat'],
                lon=log['lon'],
                acc_x=log['acc_x'],
                acc_y=log['acc_y'],
                acc_z=log['acc_z'],
                logged_at=logged_at,
                user=user,
            )
            logger.debug('log_data = %s' % log_data)
            log_data.save()

        return JsonResponse({'count': count})
    else:
        raise Http404

@login_required
def bump_chart(request):
    return render_to_response('bump_hunter/bump_chart.html', context_instance=RequestContext(request));

def logout(request):
    logout(request)
    render_to_response('bump_hunter/logout.html', context_instance=RequestContext(request))
