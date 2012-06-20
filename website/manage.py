#!/usr/bin/env python
#-*-coding:utf-8-*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flaskext.script import Manager
from dessert import config_app, dispatch_handlers, dispatch_apps
from dessert.extensions import app

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
    db.init_app(app)

    print "Drop all tables"
    db.drop_all()

    print "Create all tables"
    db.create_all()

    print "Start to add all syntax"
    from daimaduan.models import *
    from daimaduan.models.syntax import ALL_SYNTAX
    for lexer in ALL_SYNTAX:
        syntax = Syntax(lexer[0], lexer[1].lower())
        db.session.add(syntax)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    from daimaduan.models.data import pages, templates
    for page in pages:
        new_page = Page(page['slug'],
                        page['title'],
                        page['content'])
        db.session.add(new_page)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    for template in templates:
        new_temp = MessageTemplate(template['used_for'],
                                   template['title'],
                                   template['content'])
        db.session.add(new_temp)
        try:
            db.session.commit()
        except:
            db.session.rollback()

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def generate_test(config):
    config_app(app, config)

    from daimaduan.models import User, Syntax, Tag, Paste
    user1 = User(nickname='davidx',
                email='david.xie@me.com',
                password=hashPassword('123456'))
    user1.save()
    user2 = User(nickname='zhangkai',
                email='zhangkai@daimaduan.com',
                password=hashPassword('123456'))
    user2.save()
    user3 = User(nickname='guest',
                email='guest@daimaduan.com',
                password=hashPassword('123456'))
    user3.save()

    users = [user1, user2, user3]

    from tests import FILES
    import random
    for filename, syntax, tags in FILES:
        syntax = Syntax.objects(name=syntax).first()
        f = open('tests/%s' % filename, 'r')
        paste = Paste(title=filename,
                      user=users[random.randint(0, 2)],
                      syntax=syntax,
                      content=f.read())
        paste.save()
        for tag in tags:
            t = Tag.objects(name=tag).first()
            if not t:
                t = Tag(name=tag)
                t.save()
            paste.tags.append(t)
        paste.save()
        f.close()

@manager.option('-c', '--config', dest='config', help='Configuration file name')
def transfer(config):
    config_app(app, config)
    db.init_app(app)

    print "Start to add all syntax"
    from daimaduan.models import User, Syntax, Tag, Paste

    user = User(nickname=u'User', email='user@daduan.com', password='youcannotguess')
    user.save()

    import psycopg2
    import psycopg2.extras

    conn = psycopg2.connect(host='localhost', port=5432,
                            user='davidpaste', password='davidpaste', database='davidpaste')

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute("SET client_encoding TO UTF8")
    cursor.execute("select * from pastes")

    pastes = cursor.fetchall()

    for paste in pastes:
        new_paste = Paste(title=unicode(paste['title']),
                          content=unicode(paste['content']),
                          user=user,
                          created_time=paste['created_time'],
                          modified_time=paste['modified_time'],
                          view_num=paste['views'])
        cursor.execute("select name from syntax where id = %s" % paste['syntax_id'])
        syntax = cursor.fetchone()
        new_paste.syntax = Syntax.objects(name=syntax['name']).first()
        new_paste.save()

@manager.option('-c', '--config', dest='config', help='Configuration file name')
@manager.option('-e', '--email', dest='email', help='Email address')
@manager.option('-p', '--privilege', dest='privilege', help='Privilege number')
def privilege(config, email, privilege):
    config_app(app, config)
    db.init_app(app)

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

