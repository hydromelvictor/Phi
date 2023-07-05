#!/usr/bin/env python3
""" comments collections """
from . import comments
from uuid import uuid4
from datetime import datetime


def save_cmts(author, contains, postref):
    """ cmts """
    comments.insert_one({
        '_id': str(uuid4()),
        'author': author,
        'postref': postref,
        'contains': contains,
        'publish': datetime.utcnow()
    })
