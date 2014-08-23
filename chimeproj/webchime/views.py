#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
import json
import time
from time import *
import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, Context, RequestContext

from ws4py.client.threadedclient import WebSocketClient

from webchime import webchime_settings


formatter = logging.Formatter(webchime_settings.LOG_FORMAT)
h = logging.FileHandler(webchime_settings.LOG_PATH)
h.setFormatter(formatter)

logger = logging.getLogger(webchime_settings.APP_NAME)
logger.setLevel(webchime_settings.LOG_LEVEL)
logger.addHandler(h)


def error500(request):
    return render_to_response('500.html', {})


def error404(request):
    return render_to_response('404.html', {})


def visitor_1(request):
    chime_id = ''
    visitor_name = ''
    message = ''

    # get parameter
    try:
        if 'chime_id' in request.GET:
            chime_id = request.GET['chime_id']

        if 'visitor_name' in request.GET:
            visitor_name = request.GET['visitor_name']
    except:
        pass

    # notify chime.
    if chime_id != '':
        msg = {'chime_id': chime_id,
               'ipaddress': get_client_ip(request),
               'visitor_name': visitor_name}
        ret = notify_websocket('webchime', [msg])
        if ret < 0:
            message = 'fail send chime.'
        else:
            message = 'ring the chime. wait for...'
    else:
        message = '[fail call] please set chime_id.'

    return my_render_to_response(
        request,
        'visitor.html',
        {'chime_id': chime_id,
         'visitor_name': visitor_name,
         'message': message}
        )


def receiver_1(request):
    chime_id = ''

    # get parameter
    try:
        if 'chime_id' in request.GET:
            chime_id = request.GET['chime_id']
    except:
        pass

    return my_render_to_response(
        request,
        'receiver.html',
        {'chime_id': chime_id,
         'wspush_url': webchime_settings.WSPUSH_URL,
         'wspush_recvtoken': webchime_settings.WSPUSH_RECVTOKEN,
         'chime_audio_url': webchime_settings.CHIME_AUDIO_URL}
        )


def select_1(request):
    return my_render_to_response(
        request,
        'select.html',
        {}
        )


def my_render_to_response(request, template_file, paramdict):
    response = HttpResponse()

    t = loader.get_template(template_file)
    c = RequestContext(request, paramdict)
    response.write(t.render(c))
    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MyWebSocketClient(WebSocketClient):
    _is_auth = -1

    def opened(self):
        senddata = {'func': 'auth',
                    'param': {
                        'token': webchime_settings.WSPUSH_SENDTOKEN}
                    }
        self.send(json.dumps(senddata))

    def closed(self, code, reason):
        logger.info(
            "Websocket server to Closed down. (code=%s,reason=%s" %
            (code, reason))

    def received_message(self, m):
        logger.info('message received: %s' % m.data)

        try:
            convjson = json.loads(m.data)

            if convjson['func'] == 'auth':
                if convjson['statuscode'] == '200':
                    self._is_auth = 1
                    logger.info('success auth websocket server.')
                else:
                    self._is_auth = 0
                    logger.warn('fail auth websocket server.')
            else:
                pass
        except:
            logger.error('EXCEPT: recv msg (%s)' % sys.exc_info()[1])

    def sendmsg(self, markertype, markerlist):
        senddata = {'func': 'broadcast_msg',
                    'param': {'markertype': markertype,
                              'markerlist': markerlist}
                    }
        logger.info(senddata)
        self.send(json.dumps(senddata))

    def is_auth(self):
        return self._is_auth


def notify_websocket(messagetype, datalist):
    logger.debug('IN notify_websocket()')
    count = 0

    try:
        ws = MyWebSocketClient(webchime_settings.WSPUSH_URL_INTRA,
                               protocols=['http-only', 'chat'])
        ws.connect()

        while(count < webchime_settings.WSPUSH_POLLING_WAIT_MAXCOUNT):
            if ws.is_auth() < 0:
                sleep(webchime_settings.WSPUSH_POLLING_WAIT_SPAN)
                count = count + 1
            elif 0 == ws.is_auth():
                raise('fail auth websocket server.')
            else:
                ws.sendmsg(messagetype, datalist)
                logger.info('success notify websocket.')
                ws.close()
                break
    except:
        logger.error('EXCEPT: fail send websocket message (%s)' %
                     sys.exc_info()[1])
        return -1

    return 0
