#!/usr/bin/env python3
""" chatting """
from flask import Blueprint, render_template
from flask_login import current_user
from functools import wraps
from flask_socketio import disconnect
from phi import socketio
from flask_socketio import send

sms = Blueprint('sms', __name__)


def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@sms.route('/me/chat', methods=['GET'], strict_slashes=False)
def chat():
    """ chat """
    return render_template('sms/sms.html')


@socketio.on('message', namespace='/me/chat')
@authenticated_only
def handle_message_recieved(data):
    """ recieved message """
    send(data, broadcast=True)


# @socketio.on('private chat')
# @authenticated_only
# def handle_message_send(data):
#     """ send message """
#     socketio.send(data, namespace='/me/chat')


@sms.route('/me/group', methods=['GET'], strict_slashes=False)
def msg():
    """ chat """
    return render_template('sms/msg.html')


