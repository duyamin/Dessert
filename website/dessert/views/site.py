#-*-coding:utf-*-
from flask import Blueprint, render_template, g, request, abort, session, redirect, url_for, flash
from flaskext.openid import COMMON_PROVIDERS
from dessert.extensions import *
from dessert.models import *
from dessert.forms import *

siteapp = Blueprint('siteapp', __name__)

@siteapp.route('/')
def index():
    try:
        page = int(request.args.get('page', 1))
    except:
        abort(500)
    g.pagination = Post.query.paginate(1, app.config.get('PAGE_SIZE'))
    return render_template('site/index.html')

@siteapp.route('/<int:user_id>')
@siteapp.route('/<slug>')
def view(slug=None, user_id=None):
    user = getUserObject(slug=slug, user_id=user_id)
    if not user:
        abort(404)

    g.user = user
    g.pagination = Post.query.filter_by(user_id=user.id).order_by('created_time DESC').paginate(1, 20)
    return render_template('site/view.html')

@siteapp.route('/rss/<user_id>.xml')
def rss(user_id):
    pass

@siteapp.route('/page/<slug>')
def page(slug):
    pass

@siteapp.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if request.method == 'POST':
        return oid.try_login(COMMON_PROVIDERS['google'], ask_for=['email', 'nickname'])
    return render_template('site/login.html',
                           next=oid.get_next_url(),
                           error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'成功登入')
        session['user'] = str(user.id)
        session.pop('openid')
        g.user = getUserObject(user_id=session['user'])
        return redirect(url_for('siteapp.view', user_id=g.user.id))
    return redirect(url_for('siteapp.create_profile',
                            next=oid.get_next_url(),
                            nickname=resp.nickname,
                            email=resp.email))

@siteapp.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm(request.form, csrf_enabled=False)
    form.nickname.data = request.values.get('nickname')
    form.email.data = request.values.get('email')
    if request.method == 'POST' and form.validate():
        user = User(form.nickname.data,
                    form.email.data)
        user.openid = session['openid']

        db.session.add(user)
        db.session.commit()
        blog = Blog(user.id)
        blog.title = form.title.data
        db.session.add(blog)
        db.session.commit()
        flash(u'资料建立成功')
        session.pop('openid')
        return redirect(url_for('siteapp.login'))
    g.form = form
    return render_template('site/create_profile.html', next_url=oid.get_next_url())

@siteapp.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')
