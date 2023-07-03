#!/usr/bin/env python
""" init app """
from flask import Flask
from flask_tinymce import TinyMCE
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
migrate = Migrate()

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY'] = 'in-production-i-will-replace'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'Phi.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'medias')

def create_app():
    """ create flask app """
    
    tinymce = TinyMCE()
    tinymce.init_app(app)
    migrate.init_app(app, db)

    db.init_app(app)

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
    
    from .models import User, Post, Comment

    @manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    with app.app_context():
        db.create_all()

    return app
    