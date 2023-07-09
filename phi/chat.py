#!/usr/bin/env python3
""" chatting """
from flask import Blueprint, render_template
from flask_login import current_user, login_required
from functools import wraps
from flask_socketio import disconnect
from phi import socketio
from flask_socketio import send, join_room, leave_room
from .db.users import users, myrooms
from .db.chats import chats_save
from time import localtime, strftime

sms = Blueprint('sms', __name__)


def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@sms.route('/chat/<username>', methods=['GET'], strict_slashes=False)
@login_required
def chat(username):
    """ chat """

    friend = users.find_one({'username': username})
    
    room = {}
    for frd in current_user.friends:
        if frd['_id'] == friend['_id']:
            for rm in myrooms(current_user._id):
                for user in rm['users']:
                    if frd['_id'] == user['_id']:
                        room = rm
        else:
            chats_save([friend, current_user])
            for chat in myrooms(current_user._id):
                for user in chat['users']:
                    if friend['_id'] == user['_id']:
                        room = chat
            break
         
    context = {
        'current_user': current_user,
        'friend': friend,
        'room': room
    }
    return render_template('sms/sms.html', **context)


@socketio.on('message')
@authenticated_only
def message(data):
    """ recieved message """
    send({'msg': data['msg'], 'username': data['username'], 'tm': strftime('%b-%d %I:%M%p', localtime())}, room=data['room'])


@socketio.on('join')
def join(data):
    """ join """
    join_room(data['room'])
    send({'msg': data['username'] + "join" + data['room']}, room=data['room'])
    

@socketio.on('leave')
def leave(data):
    """ leave """
    leave_room(data['room'])
    send({'msg': data['username'] + "left" + data['room']}, room=data['room'])
    
