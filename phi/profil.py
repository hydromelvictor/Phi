#!/usr/bin/env python3
""" users profil """
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, send_from_directory, flash
)
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from . import app
from .const import states, jobs
from .db.comments import comments
from .db.posts import posts
from .db.users import get_user, users, myrooms
from .db.settings import settings_save, settings
from .db.friends import request_friend_to_me, friend_request, friends
from .db.chats import chats
import os

profile = Blueprint('profile', __name__)


@profile.route('/<username>/profil/overview', methods=['GET'], strict_slashes=False)
@login_required
def overview(username):
    """ overviews """
    rooms = []
    for frd in current_user.friends:
        for sms in myrooms(current_user._id):
            for rm in sms['users']:
                if frd['_id'] == rm['_id']:
                    rooms.append({'friend': frd, 'sms': sms})
    
    params = {}
    if current_user.username == username:
        params = settings.find_one({'person': current_user._id})

    myjobs = sorted(list(set(jobs)))
    from .news import friendme
    
    context = {
        'current_user': current_user,
        'country': states,
        'jobs': myjobs,
        'settings':params,
        'rooms': rooms,
        'friendme': friendme(current_user._id)
    }
    return render_template('profil/update.html', **context)


def allowed_file(filename, ext):
    """ allowed file extension """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ext


@profile.route('/img/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def image():
    """ update image profil """
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
    if request.method == 'POST':
        img = request.files.get('img')
        if img and allowed_file(img.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            user = users.find_one({'_id': current_user._id})
            users.update_one(user, {"$set": {'img': filename}})
            
            return redirect(url_for('profile.overview', username=current_user.username))
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/profil/update', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update():
    """ profil update """
    if request.method == 'POST':
        username = request.form.get('username')
        bio = request.form.get('bio')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        country = request.form.get('country')
        city = request.form.get('city')
        job = request.form.get('job')
        status = request.form.get('status')
        company = request.form.get('society')
        phone = request.form.get('phone')
        obbies = request.form.get('obbies')
        cv = request.form.get('cv')
        instagram = request.form.get('instagram')
        facebook = request.form.get('facebook')
        github = request.form.get('github')
        linkedin = request.form.get('linkedin') 
        twitter = request.form.get('twitter')
        website = request.form.get('website')
        
        user = users.find_one({'_id': current_user._id})
        users.update_one(
            user,
            {"$set": {
                'username': username,
                'bio': bio if len(bio) > 1 else '',
                'firstname': firstname if len(firstname) > 1 else '',
                'lastname': lastname if len(lastname) > 1 else '',
                'email': email,
                'country': country if len(country) > 1 else '',
                'city': city if len(city) > 1 else '',
                'job': job if len(job) > 1 else '',
                'status': status if len(status) > 1 else '',
                'company': company if len(company) > 1 else '',
                'phone': phone if len(phone) > 1 else '',
                'obbies': obbies if len(obbies) > 1 else '',
                'cv': cv if len(cv) > 1 else '',
                'instagram': instagram if len(instagram) > 1 else '',
                'facebook': facebook if len(facebook) > 1 else '',
                'github': github if len(github) > 1 else '',
                'linkedin': linkedin if len(linkedin) > 1 else '',
                'twitter': twitter if len(twitter) > 1 else '',
                'website': website if len(website) > 1 else ''
                }
            }
        )
        return redirect(url_for('profile.overview', username=current_user.username))
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/upload/<filename>')
def upload(filename):
    """ upload """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

@profile.route('/me/settings', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def parameters():
    """ settings """
    params = settings.find_one({'person': current_user._id})
    if request.method == 'POST':
        person = current_user._id
        hidden_fullname = True if request.form.get('hidden_fullname') == 'on'else False
        hidden_email = True if request.form.get('hidden_email') == 'on'else False
        hidden_country = True if request.form.get('hidden_country') == 'on'else False
        hidden_city = True if request.form.get('hidden_city') == 'on'else False
        hidden_job = True if request.form.get('hidden_job') == 'on'else False
        hidden_status = True if request.form.get('hidden_status') == 'on'else False
        hidden_society = True if request.form.get('hidden_society') == 'on'else False
        hidden_phone = True if request.form.get('hidden_phone') == 'on'else False
        hidden_obbies = True if request.form.get('hidden_obbies') == 'on'else False
        hidden_cv = True if request.form.get('hidden_cv') == 'on'else False
        hidden_social = True if request.form.get('hidden_social') == 'on' else False
        comment_disable = True if request.form.get('comment_disable') == 'on' else False
        friend_request = request.form.get('friend_request')
        profil_view = request.form.get('profil_view')
        post_comment = request.form.get('post_comment')

        if params:
            settings.update_one(
                params,
                {
                    "$set": {
                        'person': person,
                        'hideFullname': hidden_fullname,
                        'hideEmail': hidden_email,
                        'hideCountry': hidden_country,
                        'hideCity': hidden_city,
                        'hideJob': hidden_job,
                        'hideStatus': hidden_status,
                        'hideCompany': hidden_society,
                        'hidePhone': hidden_phone,
                        'hideObbies': hidden_obbies,
                        'hideCv': hidden_cv,
                        'hideSocial': hidden_social,
                        'cmtDisable': comment_disable,
                        'friendRequest': friend_request,
                        'profilView': profil_view,
                        'postComment': post_comment
                    }
                }
            )
        else:
            params = settings_save(
                person=person, 
                hideFullname=hidden_fullname,
                hideEmail=hidden_email, 
                hideCountry=hidden_country,
                hideCity=hidden_city, 
                hideJob=hidden_job,
                hideStatus=hidden_status, 
                hideCompany=hidden_society,
                hidePhone=hidden_phone, 
                hideObbies=hidden_obbies,
                hideCv=hidden_cv, 
                hideSocial=hidden_social,
                cmtDisable=comment_disable,
                friendRequest=friend_request,
                msgReceived=msg_received,
                profilView=profil_view
            )
    
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/me/pwd', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def pwd():
    """ password change """
    if request.method == 'POST':
        password = request.form.get('password')

        if current_user.check_password(password):
            newpassword = request.form.get('newpassword')
            renewpassword = request.form.get('renewpassword')

            if newpassword == renewpassword and len(newpassword) > 3:
                password_hash = generate_password_hash(newpassword, method='scrypt')
                user = users.find_one({'_id': current_user._id})
                users.update_one(
                    user,
                    {
                        "$set": {'password': password_hash}
                    }
                )
                logout_user()
                return redirect(url_for('auth.login'))
            else:
                flash('new password no equal to re-enter')
        else:
            flash('password incorrect !!!')
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/me/profil/rm', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def rm():
    """ remove account """
    if request.method == 'POST':
        if request.form.get('yes'):
            
            # delete all comments for me
            for cmtme in list(comments.find()):
                if cmtme['author'] == current_user._id:
                    comments.delete_one({'_id': cmtme['_id']})
            
            # delete all friends request for me and by me
            for req in list(friends.find()):
                if current_user._id == req['sender_id']:
                    friends.delete_one({'_id': req['_id']})
                
                if current_user._id == req['friend_id']:
                    friends.delete_one({'_id': req['_id']})
            
            # delete all comments for my posts and delete all my posts
            for postme in list(posts.find()):
                if postme['author'] == current_user._id:
                    allcmts = comments.find({'postref': postme['_id']})
                    
                    for cmt in allcmts:
                        comments.delete_one({'_id': cmt['_id']})
                    
                    posts.delete_one({'_id': postme['_id']})
            
            # delete my settings configuration
            settings.delete_one({'person': current_user._id})
            
            # remove me in the all friends of users
            for friend in current_user.friends:
                for me in friend['friends']:
                    if me['_id'] == current_user._id:
                        friend['friends'].remove(me)
            
            # delete all chat with users
            for chatme in list(chats.find()):
                for user in chatme['users']:
                    if user['_id'] == current_user._id:
                        chats.delete_one({'_id': chatme['_id']})
            
            # delete my profile picture
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.img))
            # delete me
            users.delete_one({'_id': current_user._id})
            
            return redirect(url_for('auth.sign'))
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/users/<username>', methods=['GET'], strict_slashes=False)
@login_required
def public(username):
    """ public profil """
    
    person = users.find_one({'username': username})
    params = settings.find_one({'person': person['_id']})
    
    friender = friends.find_one({'sender_id': current_user._id, 'friend_id': person['_id']})
    
    from .news import friendme
    # from .news import request_friendship
    
    context = {
        'person': person,
        'setting': params,
        'friender': friender,
        'friendme': friendme(current_user._id),
        # 'more': request_friendship(current_user._id)
    }
    return render_template('profil/view.html', **context)


@profile.route('/sendfriends', methods=['GET', 'POST'], strict_slashes=False)
def sendfriends():
    """ friends request """
    if request.method == 'POST':
        username = request.form.get('username')
        person = users.find_one({'username': username})
        
        if person:
            me = friends.find_one({'sender_id': current_user._id, 'friend_id': person['_id']})
            you = friends.find_one({'sender_id': person['_id'], 'friend_id': current_user._id})
            
            for friend in current_user.friends:
                if friend['_id'] == person['_id']:
                    return redirect(url_for('news.dash'))

            if not me and not you:
                friend_request(current_user._id, person['_id'])
                return redirect(url_for('profile.public', username=username))
            
            else:
                return redirect(url_for('news.dash'))
    return redirect(url_for('profile.overview', username=current_user.username))


@profile.route('/abortfriends', methods=['GET', 'POST'], strict_slashes=False)
def abortfriends():
    """ abort friend request """
    if request.method == 'POST':
        username = request.form.get('username')
        person = users.find_one({'username': username})
        if person:
            friends.delete_one({'sender_id': current_user._id, 'friend_id': person._id})
    return redirect(url_for('prolife.public', username=username))


@profile.route('/breakfriends', methods=['GET', 'POST'], strict_slashes=False)
def breakfriends():
    """ break friend relation """
    if request.method == 'POST':
        username = request.form.get('username')
        person = users.find_one({'username': username})
        me = users.find_one({'_id': current_user._id})
        if person:
            users.update_one(
                person,
                {
                    "$pull": {'friends': {'_id': current_user._id}}
                }
            )
            users.update_one(
                me,
                {
                    "$pull": {'friends': {'_id': person['_id']}}
                }
            )
    return redirect(url_for('profile.public', username=username))
