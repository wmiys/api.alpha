import http
import flask
from http import HTTPStatus
from ..common import security
from ..models import User

bp_users = flask.Blueprint('routeUser', __name__)

#------------------------------------------------------
# Create new user
#------------------------------------------------------
@bp_users.post('')
def usersPost():
    # set the user properties
    new_user = User(
        email      = flask.request.form.get('email') or None,
        password   = flask.request.form.get('password') or None,
        name_first = flask.request.form.get('name_first') or None,
        name_last  = flask.request.form.get('name_last') or None,
        birth_date = flask.request.form.get('birth_date') or None,
    )

    # insert the object into the database
    new_user.insert()

    # return the user object
    return flask.jsonify(new_user.get())


#------------------------------------------------------
# Get a single user
#------------------------------------------------------
@bp_users.route('<int:user_id>', methods=['GET', 'PUT'])
@security.login_required
def userGetPost(user_id):
    # make sure the user is authorized
    if flask.g.client_id != user_id:
        return ('', HTTPStatus.FORBIDDEN.value)

    user = User(id=user_id)

    if flask.request.method == 'PUT':
        # load the user's data into the object's fields
        user.fetch()

        # be sure the request body has all the correct fields
        if not user.setPropertyValuesFromDict(flask.request.form.to_dict()):  
            return ('Request body contained an invalid field', HTTPStatus.BAD_REQUEST.value) 
        
        # update the database record
        updateResultRowCount = user.update()

        # make sure there's no errors
        if updateResultRowCount not in [0, 1]:
            return ('', HTTPStatus.INTERNAL_SERVER_ERROR.value)

    # return the user object without the payout_account_id
    return flask.jsonify(user.get())