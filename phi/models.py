#!/usr/bin/env python3
""" models """
from phi import db
import os
from datetime import datetime
from uuid import uuid4
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """ user models """
    id = db.Column(db.String, primary_key=True)
    img = db.Column(db.String, nullable=False, default='img/nouser.png')
    username = db.Column(db.String(32), unique=True)
    bio = db.Column(db.Text(500))
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    firstname = db.Column(db.String(24))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String)
    country = db.Column(db.String)
    city = db.Column(db.String)
    job = db.Column(db.String(32))
    # employer ou  chomeur
    status = db.Column(db.String)
    # if employment
    society = db.Column(db.String)
    phone = db.Column(db.String)
    obbies = db.Column(db.String(501))
    cv = db.Column(db.String)
    instagram = db.Column(db.String)
    facebook = db.Column(db.String)
    github = db.Column(db.String)
    linkedin = db.Column(db.String)
    twitter = db.Column(db.String)
    website = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __init__(self, **kwargs):
        """ initialisation """
        for key, val in kwargs.items():
            if key != 'joined':
                setattr(self, key, val)
        self.joined = datetime.utcnow()
        self.id = str(uuid4())

    def __str__(self):
        """ string representation """
        return self.username
    
    @property
    def theObbies():
        """ obbies list """
        return self.obbies.split(',')
    
    @property
    def posts(self):
        """ all posts for user """
        all_posts = []
        for post in Post.query.all():
            if post.author == self.id:
                all_posts.append(post)
        return all_posts
    
    @property
    def comments(self):
        """ all comments """
        all_cmts = []
        for cmt in Comment.query.all():
            if cmt.author == self.id:
                all_cmts.append(cmt)
        return all_cmts
        


class Post(db.Model):
    """ post models """
    id = db.Column(db.String, primary_key=True)
    author = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publish = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    comments = db.relationship('Comment', backref='post')

    def __init__(self, **kwargs):
        """ initialisation """
        for key, val in kwargs.items():
                setattr(self, key, val)
        self.publish = datetime.utcnow()
        self.id = str(uuid4())
    
    @property
    def user_author(self):
        """ user author """
        return User.query.filter_by(id=self.author)
    
    def __str__(self):
        """ string representation """
        return f"{self.author}:{self.content[:30]}..."
    
    @property
    def comments(self):
        """ all comments for posts """
        all_cmts = []
        for cmt in Comment.query.all():
            if cmt.postRef == self.id:
                all_cmts.append(cmt)
        return all_cmts


class Comment(db.Model):
    """ comments model """
    id = db.Column(db.String, primary_key=True)
    author = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    postRef = db.Column(db.String, db.ForeignKey(Post.id), nullable=False)
    contains = db.Column(db.String, nullable=False)
    publish = db.Column(db.DATETIME, nullable=False, default=datetime.utcnow())
    
    def __init__(self, **kwargs):
        """ initialisation """
        for key, val in kwargs.items():
                setattr(self, key, val)
        self.publish = datetime.utcnow()
        self.id = str(uuid4())
        
    @property
    def user_cmt(self):
        """ user comment """
        return User.query.get_or_404(self.author)
