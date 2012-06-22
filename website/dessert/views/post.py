from flask import Blueprint

postapp = Blueprint('postapp', __name__)

@postapp.route('/<slug>')
def view():
    post = Post.query.filter_by(slug=slug).first()