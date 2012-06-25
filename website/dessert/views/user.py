#-*-coding:utf-*-
from flask import Blueprint, g, redirect, request, render_template
from flaskext.openid import COMMON_PROVIDERS
from dessert.extensions import *

userapp = Blueprint('userapp', __name__)

@userapp.route('/login/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if request.method == 'POST':
        return oid.try_login(COMMON_PROVIDERS['google'], ask_for=['email', 'nickname'])
    return render_template('user/login.html',
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
        return redirect(oid.get_next_url())
    return redirect(url_for('userapp.create_profile',
                            next=oid.get_next_url(),
                            nickname=resp.nickname,
                            email=resp.email))

@userapp.route('/create_profile', methods=['GET', 'POST'])
def create_profile():
    form = ProfileForm(request.form)
    form.nickname.data = request.values.get('nickname')
    form.email.data = request.values.get('email')
    if request.method == 'POST' and form.validate():
        user = User(form.nickname.data,
                    form.email.data)
        user.openid = session['openid']
        info = UserInfo(user.id)
        user.info = info
        db.session.add(user)
        db.session.add(info)
        db.session.commit()
        flash(u'资料建立成功')
        session.pop('openid')
        return redirect(url_for('userapp.login'))
    g.form = form
    return render_template('user/create_profile.html', next_url=oid.get_next_url())

@userapp.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect('/')

@userapp.route('/id/<user_id>')
@userapp.route('/<slug>')
def view(slug=None, user_id=None):
    pass
