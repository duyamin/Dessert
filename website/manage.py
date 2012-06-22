#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flaskext.script import Manager
from dessert import config_app, dispatch_handlers, dispatch_apps
from dessert.extensions import *

manager = Manager(app)

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def test(config):
    config_app(app, config)
    dispatch_handlers(app)
    dispatch_apps(app)
    app.run(host='0.0.0.0')

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def initialize(config):
    config_app(app, config)
    from dessert.models import *
    print "Drop all tables"
    db.drop_all()

    print "Create all tables"
    db.create_all()

@manager.option('-c', '--config', dest='config', help='Configuration file name')
@manager.option('-e', '--email', dest='email', help='Email address')
@manager.option('-p', '--privilege', dest='privilege', help='Privilege number')
def privilege(config, email, privilege):
    config_app(app, config)

    from daimaduan.models import User

    user = User.objects(email=email).first()
    if not user:
        print "User can not be found."
    else:
        user.privilege.privilege = int(privilege)
        user.save()
        print "Modification successed."

if __name__ == '__main__':
    manager.run()
