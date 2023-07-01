#!/usr/bin/env python3
""" chatting """
from flask import Blueprint, render_template

sms = Blueprint('sms', __name__)

@sms.route('/me', methods=['GET'], strict_slashes=False)
def chat():
    """ chat """
    return render_template('sms/sms.html')
