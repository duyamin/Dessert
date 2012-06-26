from flask import Blueprint, render_template, request, g, redirect
from dessert.extensions import db
from dessert.utils import login_required
from dessert.models import *
from dessert.forms import *

postapp = Blueprint('postapp', __name__)

@postapp.route('/id/<post_id>')
@postapp.route('/<slug>')
def view(slug=None, post_id=None):
    post = None
    if slug:
        post = Post.query.filter_by(slug=slug).first()
    elif post_id:
        post = Post.query.get_or_404(post_id)

    if not post:
        abort(404)

    g.post = post
    return render_template('post/view.html')

@postapp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate():
        post = Post(g.user.id, form.title.data, form.content.data)
        if form.slug.data:
            post.slug = form.slug.data
        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('postapp.view', id=post.id))
    g.form = form
    return render_template('post/create.html')
