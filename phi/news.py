#!/usr/bin/env python3
""" news """
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from .db.settings import settings
from .db.posts import post_cmts, post_save, posts
from .db.users import post_sender, persons, users, myrooms
from .db.comments import save_cmts
from .db.friends import request_friend_to_me, request_friend_by_me, friends
from .db.chats import chats, chats_save

from datetime import datetime
import pymongo

news = Blueprint('news', __name__)

# --- ok good ---
def friendme(sid):
    friend = []
    for fd in request_friend_to_me(sid):
        user = users.find_one({'_id': fd['sender_id']})
        friend.append(user)
    return friend


def friendbyme(sid):
    friend = []
    for fd in request_friend_by_me(sid):
        user = users.find_one({'_id': fd['friend_id']})
        friend.append(user)
    return friend


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
        'current_user': current_user,
        'friendme': friendme(current_user._id)
    }
    return render_template('news.html', **context)


@news.route('/<username>/friendship', methods=['GET'], strict_slashes=False)
def suggession(username):
    """ freind suggestion and firend request """

    # friend suggession
    sugg = []
    
    frds = []
    for fd in current_user.friends:
        frds.append(fd['_id'])
    
    for fd in friendme(current_user._id):
        frds.append(fd['_id'])
        
    for fd in friendbyme(current_user._id):
        frds.append(fd['_id'])
    
    for pers in users.find():
        
        if pers['_id'] != current_user._id:
            
            if pers['_id'] not in frds:
                
                pertinant = 0
                if pers['country'] == current_user.country:
                    pertinant += 1
                
                if pers['city'] == current_user.city:
                    pertinant += 1
                    
                if pers['job'] == current_user.job:
                    pertinant += 1
                    
                if pers['status'] == current_user.status:
                    pertinant += 1
                    
                if pers['company'] == current_user.company:
                    pertinant += 1
                    
                for i in pers['obbies'].split(','):
                    j = 0
                    if i.strip() in [h.strip() for h in current_user.obbies.split(',')]:
                        j += 1
                    if j == 4:
                        pertinant += 1
                        break
                
                for fd in pers['friends']:
                    for dd in current_user.friends:
                        if fd['_id'] == dd['_id']:
                            pertinant += 1

                if pertinant >= 4:
                    sugg.append(pers)

    context = {
        'friendme': friendme(current_user._id),
        'sugg': sugg,
    }
    
    return render_template('profil/friendship.html', **context)


@news.route('/<username>/newpost', methods=['GET'], strict_slashes=False)
@login_required
def post(username):
    """ new post """
    context = {
        'current_user': current_user,
        'friendme': friendme(current_user._id)
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
    return redirect(url_for('news.post', username=current_user.username))


@news.route('/comment', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_comments():
    """ comment """
    if request.method == 'POST':
        postref = request.form.get('postref')
        contains = request.form.get('contains')
        
        save_cmts(author=current_user._id, postref=postref, contains=contains)
        return redirect(url_for('news.dash'))
    return redirect(url_for('news.dash'))


@news.route('/<username>/posts', methods=['GET'], strict_slashes=False)
@login_required
def alls(username):
    """ all posts """
    my_posts = {}
    if current_user.username == username:
        my_posts = posts.find({'author': current_user._id}).sort('publish', pymongo.DESCENDING)

    context = {
        'my_posts': my_posts,
        'current_user': current_user,
        'friendme': friendme(current_user._id)
    }
    return render_template('post/all.html', **context)


@news.route('/users', methods=['GET'], strict_slashes=False)
@login_required
def all_users():
    """ users """
    context = {
        'current_user': current_user,
        'all_users': persons(),
        'friendme': friendme(current_user._id)
    }
    return render_template('users.html', **context)


@news.route('/users/<sender_id>/<resp>', methods=['GET'], strict_slashes=False)
@login_required
def friendresp(sender_id, resp):
    """ accept """
    req = friends.find_one({'sender_id': sender_id, 'friend_id': current_user._id})
    if req:
        if resp == 'accept':
            req['resp'] = True
            me = users.find_one({'_id': current_user._id})
            you = users.find_one({'_id': sender_id})
            
            users.update_one(
                me,
                {
                    "$push": {'friends': you}
                }
            )
            users.update_one(
                you,
                {
                    "$push": {'friends': me}
                }
            )

            chats_save([me, you])
        
        friends.delete_one({'sender_id': sender_id, 'friend_id': current_user._id})
        return redirect(url_for('news.dash'))
    return render_template('profil/friendship.html')
