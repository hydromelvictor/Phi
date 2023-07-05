#!/usr/bin/env python3
""" authentication file """
from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash
)

from flask_login import login_user, login_required, logout_user
from .db import users
from .db.users import get_user, user_save

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'], strict_slashes=True)
def login():
    """ login """
    context = {}
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        context = {
            'username': username,
            'password': password
        }
        
        if len(password) < 4:
            flash('password length less than 4')
            return render_template('auth/login.html', **context)

        if len(username) < 4:
            flash('username length less than 4')
            return render_template('auth/login.html', **context)

        user = users.find_one({'username': username})
        user = get_user(user['_id'])
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('news.dash'))
        else:
            flash('Username or password invalid')
    return render_template('auth/login.html', **context)


@auth.route('/sign', methods=['GET', 'POST'], strict_slashes=True)
def sign():
    """ register """
    context = {}
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        context = {
            'username': username,
            'email': email,
            'password': password
        }
        
        if len(username) < 4:
            flash('username length less than 4')
            return render_template('auth/sign.html', **context)
        
        user = users.find_one({'username': username})
        if user:
            flash(f'sorry {username} exists !!!')
            return render_template('auth/sign.html', **context)

        user = users.find_one({'email': email})
        if user:
            flash(f'sorry {email} exists !!!')
            return render_template('auth/sign.html', **context)
        
        if '@' not in email and len(email) < 1:
            flash('bad email')
            return render_template('auth/sign.html', **context)
        
        user_save(username=username, password=password, email=email)
        return redirect(url_for('auth.login'))
    return render_template('auth/sign.html', **context)


@auth.route('/logout', methods=['GET', 'POST'], strict_slashes=True)
@login_required
def logout():
    """ logout """
    logout_user()
    return redirect(url_for('auth.login'))
    