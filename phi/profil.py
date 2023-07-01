#!/usr/bin/env python3
""" users profil """
from flask import Blueprint, render_template


profile = Blueprint('profile', __name__)


@profile.route('/me/same_profil', methods=['GET'], strict_slashes=False)
def same():
    """ same profil """
    return render_template('profil/same.html')


@profile.route('/me/profil', methods=['GET'], strict_slashes=False)
def update():
    """ profil update """
    return render_template('profil/update.html')


@profile.route('/me/settings', methods=['GET'], strict_slashes=False)
def settings():
    """ settings """
    return render_temlate('profil/settings.html')


@profile.route('/me/profil', methods=['GET'], strict_slashes=False)
def pwd():
    """ password change """
    return render_template('profil/update.html')


@profile.route('/me/profil', methods=['GET'], strict_slashes=False)
def rm():
    """ remove account """
    return render_template('profil/update.html')
