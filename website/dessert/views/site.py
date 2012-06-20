from Flask import Blueprint, render_to_template

siteapp = Blueprint('siteapp', __name__)

@siteapp.route('/')
def index():
    return render_to_template('site/index.html')