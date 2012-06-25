#-*-coding:utf-*-
from flask import Blueprint, render_template, g
from dessert.extensions import app
from dessert.models import *

siteapp = Blueprint('siteapp', __name__)

@siteapp.route('/')
def index():
    try:
        page = int(request.args.get('page', 1))
    except:
        abort(500)
    g.pagination = Post.query.paginate(1, app.config.get('PAGE_SIZE'))
    return render_template('site/index.html')

@siteapp.route('/rss/<user_id>.xml')
def rss(user_id):
    pass
