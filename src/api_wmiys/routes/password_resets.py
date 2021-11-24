"""
Package:        password_reset
Url Prefix:     /password-resets
Description:    Update/reset a user's password
"""

import flask
from http import HTTPStatus
from wmiys_common import utilities
from ..common import security
from ..models import PasswordReset

bp_password_resets = flask.Blueprint('bp_password_resets', __name__)


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
@bp_password_resets.post('')
def getProductListings():
    # make sure the ema
    email = flask.request.form.get('email') or None
    
    if not email:
        return ('Missing required request body field: email', HTTPStatus.BAD_REQUEST)
    
    # insert the object into the database
    reset = PasswordReset(
        id    = utilities.getUUID(False),
        email = email
    )
    
    result = reset.insert()

    if not result.successful:
        return (result.error, HTTPStatus.BAD_REQUEST)

    # retrieve the record's full data from the database
    result = reset.get()

    if result.successful:
        return flask.jsonify(result.result), HTTPStatus.CREATED.value
    else:
        return (result.error, HTTPStatus.BAD_REQUEST)



    





