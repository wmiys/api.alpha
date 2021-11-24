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
    email = flask.request.form.get('email') or None
    
    if not email:
        return ('Missing required request body field: email', HTTPStatus.BAD_REQUEST)
    
    reset = PasswordReset(
        id    = utilities.getUUID(False),
        user_email = email
    )

    result = reset.insert()




    return 'password reset'






