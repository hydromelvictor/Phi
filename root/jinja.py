#!/usr/bin/env python3
""" jinja filter and templates """
from flask import Blueprint

test = Blueprint('test', __name__)


@test.app_template_test('friendEqTo')
def friendEqTo(userid:str, friends:list):
    """
    userid is str(uuid4())
    friends is List of dictionary
    return True if userid not in friends
    """
    for user in friends:
        if userid == user['_id']:
            return True
    return False


@test.app_template_test('globalFriendEqTo')
def globalFriendEqTo(user_id: str, friends:list):
    """
    userid is str(uuid4)
    friends is list of dict of list
    return True if user not in ...
    """
    for user in friends:
        if not friendNoEqTo(user_id, user['friends']):
            return False
    return True

