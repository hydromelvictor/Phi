#!/usr/bin/env python
""" init app """
import os
from flask import Flask
from flask_tinymce import TinyMCE
from flask_socketio import SocketIO
from flask_login import LoginManager

socketio = SocketIO()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY'] = 'in-production-i-will-replace'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'medias')


def create_app():
    """ create flask app """
    
    socketio.init_app(app)
    tinymce = TinyMCE()
    tinymce.init_app(app)

    from .auth import auth
    app.register_blueprint(auth)
    
    from .news import news
    app.register_blueprint(news)
    
    from .profil import profile
    app.register_blueprint(profile)
    
    from .chat import sms
    app.register_blueprint(sms)

    manager = LoginManager()
    manager.login_view = 'auth.login'
    manager.init_app(app)
    
    from .db.users import get_user

    @manager.user_loader
    def load_user(user_id):
        return get_user(user_id)

    return app
    