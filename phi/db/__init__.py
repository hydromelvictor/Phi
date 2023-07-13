#!/usr/bin/env python3
""" database """
from pymongo import MongoClient

#Client = MongoClient('mongodb+srv://hydromel:BhVMi8qg5rTgulgb@phibase.ns8wecs.mongodb.net/?retryWrites=true&w=majority')

Client = MongoClient('mongodb://localhost:27017')

db = Client.Phibase

users = db.users
friends = db.friends
posts = db.posts
comments = db.comments
settings = db.settings
chats = db.chats
