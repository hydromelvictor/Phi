#!/usr/bin/env python3
""" friends collections """
from . import friends
from datetime import datetime
from uuid import uuid4
import pymongo


# envoyer une demande d'amis
def friend_request(sender_id, friend_id, resp=False):
    """ wait list """
    friends.insert_one(
        {
            '_id': str(uuid4()),
            'sender_id': sender_id,
            'friend_id': friend_id,
            'resp': resp,
            'tm': datetime.utcnow()
        }
    )


# les demande d'amis qui m'ont ete envoyer
def request_friend_to_me(user_id):
    """ my wait freind """
    return list(friends.find({'friend_id': user_id}))
    