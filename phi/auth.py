#!/usr/bin/env python3
""" authentication file """
from flask import (
    Blueprint, render_template, redirect,
    url_for, request, flash
)
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=True)
def login():
    """ login """
    if request.method == 'POST':
        username = request.form.get('username')
        if len(username) < 4:
            flash('username length less than 4')
            return render_template('auth/login.html')
        password = request.form.get('password')
        if len(password) < 4:
            flash('password length less than 4')
            return render_template('auth/login.html')
        user = User.query.filter_by(username=username).first()
        if user and 
        
    return render_template('auth/login.html')


@auth.route('/sign', methods=['GET', 'POST'], strict_slashes=True)
def sign():
    """ register """
    return render_template('auth/sign.html')


@auth.route('/logout', methods=['GET', 'POST'], strict_slashes=True)
def logout():
    """ logout """
    return redirect(url_for('auth.login'))
    