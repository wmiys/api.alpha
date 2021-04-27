import flask
from flask import Blueprint, jsonify, request
import api_wmiys.Security as Security
from api_wmiys.Security import requestGlobals
from api_wmiys.users.User import User

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
@routeUser.route('<int:user_id>', methods=['GET'])
@Security.login_required
def userGet(user_id):
    # make sure the user is authorized
    if requestGlobals.client_id != user_id:
        flask.abort(403)

    user = User(id=user_id)
    user.fetch()

    return jsonify(user.as_dict(return_password=False))