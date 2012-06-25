from flask import Blueprint, render_template

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
    return render_template('postapp/view.html')

@postapp.route('/create')
@login_required
def create():
    pass
