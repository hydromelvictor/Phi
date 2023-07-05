#!/usr/bin/env python3
""" news """
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from .db import users, posts, settings
from .db.posts import post_cmts, post_save
from .db.users import post_sender
from .db.comments import save_cmts
from datetime import datetime
import pymongo

news = Blueprint('news', __name__)


@news.route('/', methods=['GET'], strict_slashes=False)
@login_required
def dash():
    """ news """
    allposts = posts.find().sort('publish', pymongo.DESCENDING)
    hide = False
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


@news.route('/me/new_post', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def post():
    """ new post """
    context = {
        'current_user': current_user
    }
    if request.method == 'POST':
        contains = request.form.get('tinymce')
        if len(contains) != 0 and contains != '':
            post_save(author=current_user._id, contains=contains)
            return redirect(url_for('news.dash'))
    return render_template('post/post.html', **context)


# @news.route('/me/repost', methods=['GET', 'POST'], strict_slashes=False)
# @login_required
# def repost():
#     """ repost """
    
#     context = {
#         'current_user': current_user
#     }
    
#     if request.method == 'POST':
#         post_id = request.form.get('post_id')
#         post = Post.query.get_or_404(post_id)
#         if post:
#             post.publish = datetime.utcnow()
#             repost = Repost(post_id=post.id)
#             db.session.add(repost)
#             db.session.commit()
#             return redirect(url_for('news.dash'))
#     return render_template('news.html', **context)
            

@news.route('/post/comment', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_comments():
    """ comment """

    context = {
        'current_user': current_user
    }
    
    if request.method == 'POST':
        postRef = request.form.get('postRef')
        post = post_sender({'_id': postRef})
        contains = request.form.get('contains')
        if post and len(contains) > 1:
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
    all_users = users.find().sort('username', pymongo.DESCENDING)
    context = {
        'current_user': current_user,
        'all_users': all_users
    }
    return render_template('users.html')
