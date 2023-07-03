#!/usr/bin/env python3
""" news """
from flask import Blueprint, render_template, request, redirect, url_for
from .models import User, Post, Comment
from flask_login import current_user, login_required
from phi import db

news = Blueprint('news', __name__)


@news.route('/', methods=['GET'], strict_slashes=False)
@login_required
def dash():
    """ news """
    posts = Post.query.order_by(Post.publish.desc()).all()
    news = []
    for post in posts:
        author = User.query.get_or_404(post.author)
        comments = post.comments

        cmts = []
        for cmt in comments:
            auth = User.query.get_or_404(cmt.author)
            cmts.append({'cmt': cmt, 'auth': auth})

        news.append({'post': post, 'author': author, 'cmts': cmts})
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
        content = request.form.get('tinymce')
        new_post = Post(author=current_user.id, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('news.dash'))
    return render_template('post/post.html', **context)


@news.route('/<postRef>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_comments(postRef):
    """ comment """
    post = Post.query.get_or_404(postRef)
    if request.method == 'POST':
        cmt = Comment(post=post, contains=request.form.get('contains'), user=current_user)
        db.session.add(cmt)
        db.session.commit()
    return render_template('news.html')


@news.route('/comments', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def all_comments():
    """ comment for post """
    cmts = Comment.query.order_by(Comment.publish.asc()).all()
    context = {
        'cmts': cmts
    }
    return render_template('news.html', **context)


@news.route('/comment/del/<cmt_id>', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def del_comments(cmt_id):
    """ del comment """
    cmt = Comment.query.get_or_404(cmt_id)
    if cmt:
        db.session.delete(cmt)
        db.session.commit()
    return render_template('news.html')
    

@news.route('/me/all_posts', methods=['GET'], strict_slashes=False)
@login_required
def alls():
    """ all posts """
    my_all_posts = Post.query.filter_by()
    context = {
        'my_all_posts': my_all_posts,
        'current_user': current_user
    }
    return render_template('post/all.html', **context)


@news.route('/me/users', methods=['GET'], strict_slashes=False)
@login_required
def users():
    """ users """
    all_users = User.query.all()
    context = {
        'current_user': current_user,
        'all_users': all_users
    }
    return render_template('users.html', **context)
