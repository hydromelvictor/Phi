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
    img = db.Column(db.String, nullable=False, default='nouser.png')
    username = db.Column(db.String(32), unique=True)
    bio = db.Column(db.Text(500), default='')
    joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    firstname = db.Column(db.String(24), default='')
    lastname = db.Column(db.String(64), default='')
    email = db.Column(db.String)
    country = db.Column(db.String, default='')
    city = db.Column(db.String, default='')
    job = db.Column(db.String(32), default='')
    # employer ou  chomeur
    status = db.Column(db.String, default='')
    # if employment
    society = db.Column(db.String, default='')
    phone = db.Column(db.String, default='')
    obbies = db.Column(db.String(501), default='')
    cv = db.Column(db.String, default='')
    instagram = db.Column(db.String, default='')
    facebook = db.Column(db.String, default='')
    github = db.Column(db.String, default='')
    linkedin = db.Column(db.String, default='')
    twitter = db.Column(db.String, default='')
    website = db.Column(db.String, default='')
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='user', cascade="all,delete")
    comments = db.relationship('Comment', backref='user', cascade="all,delete")

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
    comments = db.relationship('Comment', backref='post', cascade="all,delete")

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


class Settings(db.Model):
    """ account settings """
    id = db.Column(db.String, primary_key=True)
    person = db.Column(db.String, db.ForeignKey(User.id), nullable=False)
    hidden_fullname = db.Column(db.Boolean, default=False)
    hidden_email = db.Column(db.Boolean, default=False)
    hidden_country = db.Column(db.Boolean, default=False)
    hidden_city = db.Column(db.Boolean, default=False)
    hidden_job = db.Column(db.Boolean, default=False)
    hidden_status = db.Column(db.Boolean, default=False)
    hidden_society = db.Column(db.Boolean, default=False)
    hidden_phone = db.Column(db.Boolean, default=True)
    hidden_obbies = db.Column(db.Boolean, default=False)
    hidden_cv = db.Column(db.Boolean, default=False)
    hidden_social = db.Column(db.Boolean, default=False)
    comment_disable = db.Column(db.Boolean, default=False)
    
    def __init__(self, **kwargs):
        """ init """
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.id = str(uuid4())
        

class Repost(db.Model):
    """ repost """
    id = db.Column(db.String, primary_key=True)
    post_id = db.Column(db.String, db.ForeignKey(Post.id), nullable=False)

