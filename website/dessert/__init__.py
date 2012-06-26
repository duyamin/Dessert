#!/usr/bin/env python
#-*-coding:utf-8-*-
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, session, render_template, g, abort
from dessert.extensions import *
from dessert.models import User

def config_app(app, config):
    app.config.from_pyfile(config)
    db.init_app(app)
    oid.init_app(app)

    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
    file_handler = RotatingFileHandler(app.config['ERROR_LOG'],
                                       maxBytes=100000,
                                       backupCount=0)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    @app.before_request
    def before_request():
        g.user = None
        if 'user' in session:
            g.user = User.query.filter_by(id=session['user']).first()

    @app.after_request
    def after_request(response):
        try:
            db.session.commit()
        except Exception, e:
            db.session.rollback()
            #app.log.error(str(e))
            abort(500)
        return response

def dispatch_handlers(app):
    d = {}
    @app.errorhandler(403)
    def permission_error(error):
        d['title'] = u'您没有权限'
        d['message'] = u'您没有权限执行当前的操作, 请登陆或检查url是否错误.'
        return render_template('error.html', **d), 403

    @app.errorhandler(404)
    def page_not_found(error):
        d['title'] = u'页面不存在'
        d['message'] = u'您所访问的页面不存在, 是不是打错地址了啊?'
        return render_template('error.html', **d), 404

    @app.errorhandler(500)
    def page_error(error):
        d['title'] = u'页面出错啦'
        d['message'] = u'您所访问的页面出错啦! 待会再来吧!'
        return render_template('error.html', **d), 500

def dispatch_apps(app):
    from dessert.views import siteapp, postapp, userapp, adminapp
    app.register_blueprint(postapp, url_prefix='/post')
    app.register_blueprint(userapp,  url_prefix='/user')
    app.register_blueprint(adminapp, url_prefix='/admin')
    app.register_blueprint(siteapp)

    from dessert.utils import dateformat, time_passed, markdown
    app.jinja_env.filters['dateformat'] = dateformat
    app.jinja_env.filters['time_passed'] = time_passed
    app.jinja_env.filters['markdown'] = markdown
