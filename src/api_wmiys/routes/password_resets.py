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


from api_wmiys.services import password_resets as password_reset_services


bp_password_resets = flask.Blueprint('bp_password_resets', __name__)


#----------------------------------------------------------
# Create a new password reset record
#----------------------------------------------------------
@bp_password_resets.post('')
def post():
    return password_reset_services.responses_POST()


#----------------------------------------------------------
# Update an existing password reset record
#----------------------------------------------------------
@bp_password_resets.put('<uuid:password_reset_id>')
def put(password_reset_id: UUID):

    return password_reset_services.responses_PUT()



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


    





