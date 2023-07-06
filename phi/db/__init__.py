#!/usr/bin/env python3
""" database """
from pymongo import MongoClient

Client = MongoClient('mongodb://localhost:27017')
db = Client.testing

users = db.users
friends = db.friends
posts = db.posts
comments = db.comments
settings = db.settings
# chats = db.chats
# sms = db.sms
