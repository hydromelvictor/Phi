#!/usr/bin/env python3
""" database """
from pymongo import MongoClient

Client = MongoClient('mongodb://localhost:27017')
db = Client.PHI_DATABASE

users = db.users
posts = db.posts
comments = db.comments
settings = db.settings
# reposts = db.reposts
