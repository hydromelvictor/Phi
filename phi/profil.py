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
from .models import User, Post, Comment, Settings
from . import app, db
from .const import states

import os

profile = Blueprint('profile', __name__)


@profile.route('/me/profil/overview', methods=['GET'], strict_slashes=False)
@login_required
def overview():
    """ overviews """
    settings = Settings.query.filter_by(person=current_user.id).first()
    posts = Post.query.filter_by(author=current_user.id).order_by(Post.publish)
    context = {
        'current_user': current_user,
        'country': states,
        'posts': posts,
        'settings':settings
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
        'country': states,
        'settings':settings
    }
    return render_template('profil/update.html', **context)


@profile.route('/upload/<filename>')
def upload(filename):
    """ upload """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

@profile.route('/me/settings', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def settings():
    """ settings """
    settings = Settings.query.filter_by(person=current_user.id).first()
    if request.method == 'POST':
        person = current_user.id
        hidden_fullname = True if request.form.get('hidden_fullname') == 'on'else False
        hidden_email = True if request.form.get('hidden_email') == 'on'else False
        hidden_country = True if request.form.get('hidden_country') == 'on'else False
        hidden_city = True if request.form.get('hidden_city') == 'on'else False
        hidden_job = True if request.form.get('hidden_job') == 'on'else False
        hidden_status = True if request.form.get('hidden_status') == 'on'else False
        hidden_society = True if request.form.get('hidden_society') == 'on'else False
        hidden_phone = True if request.form.get('hidden_phone') == 'on'else False
        hidden_obbies = True if request.form.get('hidden_obbies') == 'on'else False
        hidden_cv = True if request.form.get('hidden_cv') == 'on'else False
        hidden_social = True if request.form.get('hidden_social') == 'on' else False
        comment_disable = True if request.form.get('comment_disable') == 'on' else False
        settings = Settings(
            person=person,
            hidden_fullname=hidden_fullname,
            hidden_email=hidden_email,
            hidden_country=hidden_country,
            hidden_city=hidden_city,
            hidden_job=hidden_job,
            hidden_status=hidden_status,
            hidden_society=hidden_society,
            hidden_phone=hidden_phone,
            hidden_obbies=hidden_obbies,
            hidden_cv=hidden_cv,
            hidden_social=hidden_social,
            comment_disable=comment_disable
        )
        
        db.session.add(settings)
        db.session.commit()
        return redirect(url_for('profile.overview'))
    context = {
        'current_user': current_user,
        'settings':settings
    }
    return render_template('profil/update.html', **context)


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


@profile.route('/me/profil/rm', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def rm():
    """ remove account """
    if request.method == 'POST':
        if request.form.get('yes'):
            posts = Post.query.all()
            cmts = Comment.query.all()
            
            # delete all post for current_user
            for post in posts:
                # delete all comments of post
                for cmt in cmts:
                    if cmt.postRef == post.id:
                        db.session.delete(cmt)
                # delete post
                if post.author == current_user.id:
                    db.session.delete(post)

            #delete all comments for current_user
            for cmt in cmts:
                if cmt.author == current_user.id:
                    db.session.delete(cmt)

            db.session.delete(User.query.get_or_404(current_user.id))
            db.session.commit()
            return redirect(url_for('auth.sign'))
    context = {
        'current_user': current_user
    }
    return render_template('profil/update.html', **context)


@profile.route('/users/<username>', methods=['GET'], strict_slashes=False)
@login_required
def public(username):
    """ public profil """
    person = User.query.filter_by(username=username).first()
    setting = Settings.query.filter_by(person=person.id).first()
    context = {
        'person': person,
        'setting': setting
    }
    return render_template('profil/view.html', **context)
