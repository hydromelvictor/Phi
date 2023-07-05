#!/usr/bin/env python3
""" database """
from pymongo import MongoClient

Client = MongoClient('mongodb://localhost:27017')
db = Client.phibase

users = db.users
posts = db.posts
comments = db.comments
settings = db.settings
