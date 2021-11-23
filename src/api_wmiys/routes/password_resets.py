"""
Package:        password_reset
Url Prefix:     /password-resets
Description:    Update/reset a user's password
"""

import flask
from http import HTTPStatus
from ..common import security

bp_password_resets = flask.Blueprint('bp_password_resets', __name__)


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
@bp_password_resets.post('')
# @security.login_required
def getProductListings():
    return 'password reset'






