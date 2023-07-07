#!/usr/bin/env python3
""" chats collections """
from . import chats
from datetime import datetime
from uuid import uuid4


def chats_save(users):
    """ chat """
    chats.insert_one(
        {
            '_id': str(uuid4()),
            'publish': datetime.utcnow(),
            'users': users,
            'sms': []
        }
    )
