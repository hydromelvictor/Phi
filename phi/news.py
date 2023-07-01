#!/usr/bin/env python3
""" news """
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Post
from flask_login import current_user, login_required
from phi import db

news = Blueprint('news', __name__)


@news.route('/', methods=['GET'], strict_slashes=False)
@login_required
def dash():
    """ news """
    posts = db.session.execute(db.select(Post))
    context = {
        'posts': posts,
        'current_user': current_user
    }
    return render_template('news.html', **context)


@news.route('/me/new_post', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def post():
    """ new post """
    context = {
        'current_user': current_user
    }
    if request.method == 'POST':
        content = request.form.get('tinymce')
        new_post = Post(author=current_user.id, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('news.dash'))
    return render_template('post/post.html', **context)


@news.route('/me/all_posts', methods=['GET'], strict_slashes=False)
@login_required
def alls():
    """ all posts """
    my_all_posts = db.session.execute(db.select(Post).filter_by(id=current_user.id)).scalar()
    context = {
        'my_all_posts': my_all_posts,
        'current_user': current_user
    }
    return render_template('post/all.html', **context)


@news.route('/me/all_posts', methods=['GET'], strict_slashes=False)
@login_required
def users():
    """ users """
    all_users = db.session.execute(db.select(User).order_by(User.username)).scalar()
    context = {
        'current_user': current_user,
        'all_users': all_users
    }
    return render_template('users.html', **context)
