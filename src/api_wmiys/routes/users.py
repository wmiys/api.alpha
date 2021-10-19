import http
import flask
from http import HTTPStatus
from ..common import security
from ..models import User

routeUser = flask.Blueprint('routeUser', __name__)

#------------------------------------------------------
# Create new user
#------------------------------------------------------
@routeUser.route('', methods=['POST'])
def usersPost():
    new_user = User()

    # set the user properties
    new_user.email      = flask.request.form.get('email') or None
    new_user.password   = flask.request.form.get('password') or None
    new_user.name_first = flask.request.form.get('name_first') or None
    new_user.name_last  = flask.request.form.get('name_last') or None
    new_user.birth_date = flask.request.form.get('birth_date') or None
    
    new_user.insert()
    new_user.fetch()

    return flask.jsonify(new_user.__dict__)


#------------------------------------------------------
# Get a single user
#------------------------------------------------------
@routeUser.route('<int:user_id>', methods=['GET', 'PUT'])
@security.login_required
def userGetPost(user_id):
    # make sure the user is authorized
    if security.requestGlobals.client_id != user_id:
        return ('', HTTPStatus.FORBIDDEN.value)

    user = User(id=user_id)
    user.fetch()

    if flask.request.method == 'PUT':
        # be sure the request body has all the correct fields
        if not user.setPropertyValuesFromDict(flask.request.form.to_dict()):  
            return ('Request body contained an invalid field', HTTPStatus.BAD_REQUEST.value) 
        
        updateResultRowCount = user.update()

        if updateResultRowCount not in [0, 1]:
            return ('', HTTPStatus.INTERNAL_SERVER_ERROR.value)

    return flask.jsonify(user.as_dict(return_password=False))