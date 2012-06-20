from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.openid import OpenID
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()
oid = OpenID()