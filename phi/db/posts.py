#!/usr/bin/env python3
""" posts collections """
from . import posts
from .comments import comments
from uuid import uuid4
from datetime import datetime
import pymongo


def post_save(author, contains):
    """ create posts """
    posts.insert_one(
        {
            '_id': str(uuid4()),
            'author': author,
            'contains': contains,
            'publish': datetime.utcnow()
        }
    )


def post_cmts(post_id):
    """ post comment """
    return comments.find({'postref': post_id}).sort('publish', pymongo.DESCENDING)
