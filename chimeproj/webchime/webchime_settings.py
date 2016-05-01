#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

APP_ROOT = os.path.realpath(os.path.dirname(__file__))
APP_NAME = 'webchime'
MOUNT_PREFIX = '/webchime'

APP_STATIC_ROOT = '%s/static/' % (APP_ROOT,)
APP_STATIC_SITE = '/static/%s/' % (APP_NAME,)

LOG_LEVEL = logging.INFO
LOG_PATH = '%s/webchime.log' % '/var/log/webchime'
#LOG_PATH = '%s/log/markerstorage.log' % os.environ.get('HOME')
LOG_FORMAT = '%(asctime)s,%(levelname)-8s,%(message)s'

WSPUSH_URL = 'ws://pcdennokan.dip.jp:8888'
WSPUSH_URL_INTRA = 'ws://192.168.22.102:8888'
WSPUSH_RECVTOKEN = '12345678'
WSPUSH_SENDTOKEN = 'abcdefgh'
WSPUSH_POLLING_WAIT_SPAN = 0.1
WSPUSH_POLLING_WAIT_MAXCOUNT = 50

CHIME_AUDIO_URL = 'http://pcdennokan.dip.jp/static/se_maoudamashii_chime13.mp3'

try:
    from .webchime_settings_devel import *
except:
    pass
