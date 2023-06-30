#!/usr/bin/env python
""" init app """
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """ create flask app """
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['SECRET_KEY'] = 'in-production-i-will-replace'
    
    db.init_app(app)
    
    from .auth import auth
    app.register_blueprint(auth)
    
    manager = LoginManager()
    manager.login_view = 'auth.login'
    manager.init_app(app)
    
    from .models import User

    @manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    
    with app.app_context():
        db.create_all()

    return app
    