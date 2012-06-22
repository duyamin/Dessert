from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.openid import OpenID
from flaskext.gravatar import Gravatar

app = Flask(__name__)
db = SQLAlchemy()
oid = OpenID()
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False)