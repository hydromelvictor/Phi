#!/usr/bin/env python3
""" users profil """
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, send_from_directory, flash
)
from flask_login import (
    login_required, current_user, logout_user
)
from werkzeug.utils import secure_filename
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from .models import User
from . import app, db
from .const import states

import os

profile = Blueprint('profile', __name__)


@profile.route('/me/profil/overview', methods=['GET'], strict_slashes=False)
@login_required
def overview():
    """ overviews """

    context = {
        'current_user': current_user,
        'country': states
    }
    return render_template('profil/update.html', **context)


def allowed_file(filename, ext):
    """ allowed file extension """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ext


@profile.route('/me/profil/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update():
    """ profil update """
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    if request.method == 'POST':
        img = request.files.get('img')
        if img and allowed_file(img.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.img = filename
        
        current_user.username = request.form.get('username')
        current_user.bio = request.form.get('bio')
        current_user.firstname = request.form.get('firstname')
        current_user.lastname = request.form.get('lastname')
        current_user.email = request.form.get('email')
        current_user.country = request.form.get('country')
        current_user.city = request.form.get('city')
        current_user.job = request.form.get('job')
        current_user.status = request.form.get('status')
        current_user.society = request.form.get('society')
        current_user.phone = request.form.get('phone')
        current_user.obbies = request.form.get('obbies')
        current_user.cv = request.form.get('cv')
        current_user.instagram = request.form.get('instagram')
        current_user.facebook = request.form.get('facebook')
        current_user.github = request.form.get('github')
        current_user.linkedin = request.form.get('linkedin') 
        current_user.twitter = request.form.get('twitter')
        current_user.website = request.form.get('website')
        
        db.session.commit()
        return redirect(url_for('profile.overview'))
    context = {
        'current_user': current_user,
        'country': states
    }
    return render_template('profil/update.html', **context)


@profile.route('/upload/<filename>')
def upload(filename):
    """ upload """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

@profile.route('/<user_id>/settings', methods=['GET'], strict_slashes=False)
@login_required
def settings(user_id):
    """ settings """
    context = {
        'current_user': current_user
    }
    return render_template('profil/settings.html', **context)


@profile.route('/me/pwd', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def pwd():
    """ password change """
    if request.method == 'POST':
        password = request.form.get('password')
        if check_password_hash(current_user.password, password):
            newpassword = request.form.get('newpassword')
            renewpassword = request.form.get('renewpassword')
            if newpassword == renewpassword and len(newpassword) > 3:
                current_user.password = generate_password_hash(newpassword, method='scrypt')
                logout_user()
                return redirect(url_for('auth.login'))
            else:
                flash('new password no equal to re-enter')
        else:
            flash('password incorrect !!!')
    context = {
        'current_user': current_user
    }
    return render_template('profil/update.html', **context)


@profile.route('/<user_id>/profil/rm', methods=['GET'], strict_slashes=False)
@login_required
def rm(user_id):
    """ remove account """
    context = {
        'current_user': current_user
    }
    return render_template('profil/update.html', **context)


@profile.route('/<username>/profil', methods=['GET'], strict_slashes=False)
@login_required
def view(username):
    """ profil view """
    return render_template('profil/view.html')
