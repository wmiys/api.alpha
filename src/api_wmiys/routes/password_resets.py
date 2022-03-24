"""
Package:        password_reset
Url Prefix:     /password-resets
Description:    Update/reset a user's password
"""

from uuid import UUID
import flask
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

    return password_reset_services.responses_PUT(password_reset_id)


    





