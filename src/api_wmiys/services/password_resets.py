"""
**********************************************************************************************

Business logic for password resets.

There are 2 endpoints for password resets:
    - post
    - put


To reset a User's password:
    - they need to send a POST request to tell the API that they would to reset their password
        - must provide the email registered to their account
    - the API will then record it in the database and return a UUID of the password reset record
    - once User's have the password reset id, 
        - they can then send a PUT request with the ID in the URI
        - provide the new password 

**********************************************************************************************
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from uuid import UUID

import flask

from api_wmiys.domain import models
from api_wmiys.repository import password_resets as password_resets_repo
from api_wmiys.common import serializers
from api_wmiys.common import responses
from wmiys_common import utilities


class BadRequestErrorMessages(str, Enum):
    MISSING_EMAIL    = 'Missing required request body field: email'
    MISSING_PASSWORD = 'Missing required request body field: password'


PASSWORD_RESET_MODEL_PASSWORD_FIELD = 'password'


NUM_MINS_EXPIRED = 30


#----------------------------------------------------------
# Update an existing password reset record
#----------------------------------------------------------
def responses_PUT(password_reset_id: UUID) -> flask.Response:
    # create a PasswordReset model to send to the repository
    new_reset = _createNewModel(password_reset_id)

    # utilities.dumpJson(new_reset)


    # make sure the client provided the new password
    if not new_reset.password:
        return responses.badRequest(BadRequestErrorMessages.MISSING_PASSWORD)

    # record the updated data in the database
    db_result = password_resets_repo.update(new_reset, NUM_MINS_EXPIRED)

    # if not db_result.successful:
    #     return responses.badRequest(str(db_result.error))


    utilities.dumpJson(db_result)


    # # make sure the password reset record exists and was created at most 30 minutes ago
    # if db_result.data != 1:
    #     return responses.notFound()


    # # now, need to update the User's password

    # new_password = new_reset.password











    

    # return responses.updated(db_result)


    # return the json object
    return _standardResponse(new_reset, responses.updated)

    
    return 'password reset: PUT'


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
def responses_POST() -> flask.Response:
    # create a new PasswordReset model to send to the repository
    new_reset = _createNewModel(utilities.getUUID(False))

    # make sure the client provided their email
    if not new_reset.email:
        return responses.badRequest(BadRequestErrorMessages.MISSING_EMAIL)

    # record the data in the database
    db_result = password_resets_repo.insert(new_reset)

    if not db_result.successful:
        return responses.badRequest(str(db_result.error))

    # return the json object
    return _standardResponse(new_reset, responses.created)


#----------------------------------------------------------
# Construct a new PasswordReset model to be inserted into the database
# The email/password values are provided in the request's form
#----------------------------------------------------------
def _createNewModel(password_reset_id: UUID) -> models.PasswordReset:
    form = flask.request.form.to_dict()

    reset = models.PasswordReset(
        id         = password_reset_id,
        email      = form.get('email') or None,
        created_on = datetime.now(),
        password   = form.get(PASSWORD_RESET_MODEL_PASSWORD_FIELD) or None,
        updated_on = datetime.now(),
    )

    return reset


#----------------------------------------------------------
# Standardized response routine that returns the given PasswordReset
#
# Args:
#   password_reset: the object to be returned
#   responses_callback: api_wmiys.common.responses callback
#----------------------------------------------------------
def _standardResponse(password_reset: models.PasswordReset, responses_callback) -> flask.Response:
    output = _toDictNoPassword(password_reset)
    return responses_callback(output)

#----------------------------------------------------------
# Transform the given PasswordReset model into a dictionary with no new_password key
#----------------------------------------------------------
def _toDictNoPassword(password_reset: models.PasswordReset) -> dict:
    # Transform the model into a dictionary
    reset_dict = dict(password_reset.__dict__)
    
    # remove the new_password key/value pair
    reset_dict.pop(PASSWORD_RESET_MODEL_PASSWORD_FIELD)

    return reset_dict


