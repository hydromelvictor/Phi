#!/usr/bin/env python3
""" users profil """
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User

profile = Blueprint('profile', __name__)


@profile.route('/me/same_profil', methods=['GET'], strict_slashes=False)
@login_required
def same():
    """ same profil """
    jobs_users = []
    if current_user.job:
        jobs_users = User.query.filter_by(job=current_user.job)
    return render_template('profil/same.html')


@profile.route('/<user_id>/profil', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def update(user_id):
    """ profil update """
    file = 'Phi/jobs.csv'
    jobs = []
    with open(file, 'r') as file:
        ls = file.readlines()
        for l in ls:
            jobs.append(l.split('-')[0])
        jobs = list(set(jobs))

    context = {
        'current_user': current_user,
        'jobs': jobs
    }
    return render_template('profil/update.html', **context)


@profile.route('/<user_id>/settings', methods=['GET'], strict_slashes=False)
@login_required
def settings(user_id):
    """ settings """
    context = {
        'current_user': current_user
    }
    return render_temlate('profil/settings.html', **context)


@profile.route('/<user_id>/profil/pwd', methods=['GET'], strict_slashes=False)
@login_required
def pwd(user_id):
    """ password change """
    context = {
        'current_user': current_user
    }
    return render_template('profil/update.html', **context)


@profile.route('/<user_id>/profil/rm', methods=['GET'], strict_slashes=False)
@login_required
def rm(user_id):
    """ remove account """
    context = {
        'current_user': current_user
    }
    return render_template('profil/update.html', **context)
