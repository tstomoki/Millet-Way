# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from bump_hunter.models import LogData

import json
import logging
import time
import datetime
import tweepy
# Authentication Information for @bumps_hunter
## https://twitter.com/bumps_hunter
CONSUMER_KEY        = "QJhFqZOPE9xDRb90ZYUhCaHw2"
CONSUMER_SECRET     = "YErkMoxOmXTmIwqb1QyOO2cP0ZwovXcJeOM9vgcMX7mJKt4MiJ"
ACCESS_TOKEN        = "3315641186-dV9VB8PwJt5eCmyFuFrXrkNNVmYyTVDOXoXmbWx"
ACCESS_TOKEN_SECRET = "Ou9LUOHjfyONE3jtFIoHuuMaqpNlVdzkyeWmmyxDDAgZV"


logger = logging.getLogger(__name__)

@login_required
def bump_map(request):
    return render_to_response('bump_hunter/bump_map.html',  # 使用するテンプレート
                              context_instance=RequestContext(request))  # その他標準のコンテキスト

# tweet method
@login_required
def bump_tweet(request):
    # Oauth authenticate
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    # post tweet
    api.update_status(status='Updating using OAuth authentication via Tweepy!')
    
    return render_to_response('bump_hunter/bump_map.html',  # 使用するテンプレート
                              context_instance=RequestContext(request))  # その他標準のコンテキスト

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
