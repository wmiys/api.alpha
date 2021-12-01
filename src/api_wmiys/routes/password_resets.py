"""
Package:        password_reset
Url Prefix:     /password-resets
Description:    Update/reset a user's password
"""

from uuid import UUID
from datetime import datetime
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
def post():
    # make sure the request body contains the email field
    email = flask.request.form.get('email') or None
    if not email:
        return ('Missing required request body field: email', HTTPStatus.BAD_REQUEST.value)
    
    # insert the object into the database
    reset = PasswordReset(
        id         = utilities.getUUID(False),
        email      = email,
        created_on = datetime.now()
    )
    
    result = reset.insert()

    if not result.successful:
        return (result.error, HTTPStatus.BAD_REQUEST.value)

    # retrieve the record's full data from the database
    result = reset.get()

    if result.successful:
        return (flask.jsonify(result.result), HTTPStatus.CREATED.value)
    else:
        return (result.error, HTTPStatus.BAD_REQUEST)


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
@bp_password_resets.put('<uuid:password_reset_id>')
def put(password_reset_id: UUID):
    # make sure the request body contains the password field
    new_password = flask.request.form.get('password') or None
    if not new_password:
        return ('Missing required request body field: password', HTTPStatus.BAD_REQUEST)

    # load up the password reset object's values
    passwordReset = PasswordReset(id=password_reset_id)
    passwordReset.load()

    is_updateable = passwordReset.canPasswordBeReset()
    
    if is_updateable:
        return is_updateable

    passwordReset.new_password = new_password
    update_result = passwordReset.update()

    if not update_result.successful:
        return (update_result.error, HTTPStatus.BAD_REQUEST)

    return ('', HTTPStatus.OK)


    





