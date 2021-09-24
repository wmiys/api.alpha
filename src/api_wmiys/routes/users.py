import flask
from flask import Blueprint, jsonify, request
import api_wmiys.common.Security as Security
from api_wmiys.common.Security import requestGlobals
from ..models import User

routeUser = Blueprint('routeUser', __name__)

#------------------------------------------------------
# Create new user
#------------------------------------------------------
@routeUser.route('', methods=['POST'])
def usersPost():
    new_user = User()

    # set the user properties
    new_user.email      = request.form.get('email') or None
    new_user.password   = request.form.get('password') or None
    new_user.name_first = request.form.get('name_first') or None
    new_user.name_last  = request.form.get('name_last') or None
    new_user.birth_date = request.form.get('birth_date') or None
    
    new_user.insert()
    new_user.fetch()

    return jsonify(new_user.__dict__)


#------------------------------------------------------
# Get a single user
#------------------------------------------------------
@routeUser.route('<int:user_id>', methods=['GET', 'PUT'])
@Security.login_required
def userGetPost(user_id):
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    user = User(id=user_id)
    user.fetch()

    if request.method == 'PUT':
        # be sure the request body has all the correct fields
        if not user.setPropertyValuesFromDict(request.form.to_dict()):  
            return ('Request body contained an invalid field', 400) 
        
        updateResultRowCount = user.update()

        if updateResultRowCount not in [0, 1]:
            flask.abort(500)

    return jsonify(user.as_dict(return_password=False))