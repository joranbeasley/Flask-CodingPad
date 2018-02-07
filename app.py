from flask import Flask
# from flask_login import login_manager

from filters import MyFilters
from models import db,login_manager
from socket_server import socketio
from views import flask_views
from api import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!ShhHHHHH!!!@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
app.config['debug'] = True
app.register_blueprint(flask_views)
app.register_blueprint(api,url_prefix="/api")
db.app = app
db.init_app(db.app)
socketio.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "do_login"
MyFilters.init_app(app)