#!/usr/bin/env python
#-*-coding:utf-8-*-
from flask import request, session, url_for, redirect, abort, send_file, g
from functools import wraps
import hashlib
import re
from datetime import datetime
from markdown import markdown as mk

def dateformat(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user:
            return redirect(url_for('userapp.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def time_passed(value):
    now = datetime.now()
    past = now - value
    if past.days:
        return u'%s天前' % past.days
    mins = past.seconds / 60
    if mins < 60:
        return u'%s分钟前' % mins
    hours = mins / 60
    return u'%s小时前' % hours

def markdown(value):
    return mk(value)