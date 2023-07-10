#!/usr/bin/env pythpn3
""" settings collection """
from . import settings
from uuid import uuid4


def settings_save(
    person, hideFullname=False, hideEmail=False,
    hideCountry=False, hideCity=False, hideJob=False,
    hideStatus=False, hideCompany=False, hidePhone=False,
    hideObbies=False, hideCv=False, hideSocial=False,
    cmtDisable=False, friendRequest=False, msgReceived=False,
    profilView=False, postComment=False
    ):
    """ settings save """
    settings.insert_one({
        '_id': str(uuid4()),
        'person': person,
        'hideFullname': hideFullname,
        'hideEmail': hideEmail,
        'hideCountry': hideCountry,
        'hideCity': hideCity,
        'hideJob': hideJob,
        'hideStatus': hideStatus,
        'hideCompany' : hideCompany,
        'hidePhone' : hidePhone,
        'hideObbies' : hideObbies,
        'hideCv' : hideCv,
        'hideSocial' : hideSocial,
        'cmtDisable' : cmtDisable,
        'friendRequest': friendRequest,
        'profilView': profilView,
        'postComment': postComment
    })
