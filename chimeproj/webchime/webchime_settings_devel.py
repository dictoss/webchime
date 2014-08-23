#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

APP_ROOT = os.path.realpath(os.path.dirname(__file__))
APP_NAME = 'webapp'
MOUNT_PREFIX = ''

APP_STATIC_ROOT = '%s/static/' % (APP_ROOT,)
APP_STATIC_SITE = '/static/%s/' % (APP_NAME,)

LOG_LEVEL = logging.DEBUG
LOG_PATH = '%s/log/webchime.log' % os.environ.get('HOME')
LOG_FORMAT = '%(asctime)s,%(levelname)-8s,%(message)s'

WSPUSH_URL = 'ws://192.168.22.102:8888'
WSPUSH_URL_INTRA = 'ws://192.168.22.102:8888'
WSPUSH_RECVTOKEN = '12345678'
WSPUSH_SENDTOKEN = 'abcdefgh'
WSPUSH_POLLING_WAIT_SPAN = 0.1
WSPUSH_POLLING_WAIT_MAXCOUNT = 50

CHIME_AUDIO_URL = 'http://192.168.22.30/static/se_maoudamashii_chime13.mp3'
