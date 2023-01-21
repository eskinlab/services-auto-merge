#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import time


def timestamp():
    get_time = time.time()
    ts = datetime.datetime.fromtimestamp(get_time).strftime('%Y-%m-%d %H:%M:%S')
    return ts


class msg(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDCOLOR = '\033[0m'
    TIMESTAMP = timestamp()

    @staticmethod
    def info(message):
        return f'{msg.BLUE}[{msg.TIMESTAMP}][INFO] {message} {msg.ENDCOLOR}'

    @staticmethod
    def ok(message):
        return f'{msg.GREEN}[{msg.TIMESTAMP}][OK] {message} {msg.ENDCOLOR}'

    @staticmethod
    def warn(message):
        return f'{msg.YELLOW}[{msg.TIMESTAMP}][WARN] {message} {msg.ENDCOLOR}'

    @staticmethod
    def error(message):
        return f'{msg.RED}[{msg.TIMESTAMP}][ERROR] {message} {msg.ENDCOLOR}'
