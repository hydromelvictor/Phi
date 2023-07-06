#!/usr/bin/env python3
""" users collection """

from . import users, settings
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """ user """
    
    def __init__(
        self, _id, username, email, password, img, bio, joined,
        firstname, lastname, country, city, job, status,
        company, phone, obbies, cv, instagram, facebook,
        github, linkedin, twitter, website, friends
        ):
        """ init """
        self._id = _id
        self.username = username
        self.email = email
        self.password = password
        self.img = img
        self.bio = bio
        self.joined = joined
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.city = city
        self.job = job
        self.status = status
        self.company = company
        self.phone = phone
        self.obbies = obbies
        self.cv = cv
        self.instagram = instagram
        self.facebook = facebook
        self.github = github
        self.linkedin = linkedin
        self.twitter = twitter
        self.website = website
        self.friends = friends
    
    @staticmethod
    def is_authenticated(self):
        """ user authentication """
        return True
    
    @staticmethod
    def is_active(self):
        """ active user """
        return True
    
    @staticmethod
    def is_anonymous(self):
        """ anonymous user """
        return False
    
    def get_id(self):
        """ user_id """
        return self._id
    
    def check_password(self, password_input):
        """ verified password """
        return check_password_hash(self.password, password_input)
        

def user_save(
    username, password, img='nouser.png', bio='', firstname='',
    lastname='', email='', country='', city='', job='',
    status='', company='', phone='', obbies='', cv='',
    instagram='', facebook='', github='', linkedin='',
    twitter='', website='', friends=[]
    ):
    """ create new user """
    users.insert_one({
        '_id': str(uuid4()),
        'img': img,
        'username': username,
        'bio': bio,
        'joined': datetime.utcnow(),
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'country': country,
        'city': city,
        'job': job,
        'status' : status,
        'company': company,
        'phone': phone,
        'obbies': obbies,
        'cv': cv,
        'instagram': instagram,
        'facebook': facebook,
        'github': github,
        'linkedin': linkedin,
        'twitter': twitter,
        'website': website,
        'friends': friends,
        'password': generate_password_hash(password, method='scrypt')
    })


def get_user(user_id):
    """ user search """
    user = users.find_one({'_id': user_id})
    return User(
        user['_id'], user['username'], user['email'], user['password'],
        user['img'], user['bio'], user['joined'], user['firstname'],
        user['lastname'], user['country'], user['city'], user['job'],
        user['status'], user['company'], user['phone'], user['obbies'],
        user['cv'], user['instagram'], user['facebook'], user['github'],
        user['linkedin'], user['twitter'], user['website'], user['friends']
    ) if user else None


def post_sender(sender_id):
    """ user of post """
    return users.find_one({'_id': sender_id})


def persons():
    """ all users """
    return users.find()


def user_params(user_id):
    """ parameters """
    return settings.find_one({'person': user_id})
