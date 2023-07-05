#!/usr/bin/env python3
""" news """
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .db import users, posts, settings
from .db.posts import post_cmts, post_save
from .db.users import post_sender, persons
from .db.comments import save_cmts
from datetime import datetime
import pymongo

news = Blueprint('news', __name__)


@news.route('/', methods=['GET'], strict_slashes=False)
@login_required
def dash():
    """ news """
    allposts = posts.find().sort('publish', pymongo.DESCENDING)
    news = []
    for post in allposts:
        author = post_sender(post['author'])
        
        cmts = []
        for cmt in post_cmts(post['_id']):
            auth = users.find_one({'_id': cmt['author']})
            cmts.append({'cmt': cmt, 'auth': auth})

        hide = settings.find_one({'person': author['_id']})

        news.append({'post': post, 'author': author, 'cmts': cmts, 'hide': hide})

    context = {
        'news': news,
        'current_user': current_user
    }
    return render_template('news.html', **context)


@news.route('/<username>/newpost', methods=['GET'], strict_slashes=False)
@login_required
def post(username):
    """ new post """
    context = {
        'current_user': current_user
    }
    return render_template('post/post.html', **context)


@news.route('/post', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def newpost():
    """ new post """
    if request.method == 'POST':
        contains = request.form.get('tinymce')
        if len(contains) != 0 and contains != '':
            post_save(author=current_user._id, contains=contains)
            return redirect(url_for('news.dash'))
    return render_template('post/post.html', **context)


@news.route('/comment', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_comments():
    """ comment """
    if request.method == 'POST':
        postRef = request.form.get('postRef')
        post = post_sender({'_id': postRef})
        contains = request.form.get('contains')
        if post:
            save_cmts({'author': current_user._id, 'postref': postRef, 'contains': contains})
            return redirect(url_for('news.dash'))
        return redirect(url_for('news.dash'))
    return render_template('news.html', **context)


@news.route('/me/all_posts', methods=['GET'], strict_slashes=False)
@login_required
def alls():
    """ all posts """
    my_posts = posts.find({'author': current_user._id}).sort('publish', pymongo.DESCENDING)
    context = {
        'my_posts': my_posts,
        'current_user': current_user
    }
    return render_template('post/all.html', **context)


@news.route('/me/users', methods=['GET'], strict_slashes=False)
@login_required
def all_users():
    """ users """
    context = {
        'current_user': current_user,
        'all_users': persons()
    }
    return render_template('users.html', **context)
