from __future__ import annotations
import flask
from functools import wraps
from wmiys_common import keys
from ..db import DB

CLIENT_CUSTOM_HEADER_KEY = 'x-client-key'


#------------------------------------------------------
# Verifies that:
#   - client request has basic authentication header fields
#   - the credentials are correct
#------------------------------------------------------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        if not flask.request.authorization:
            flask.abort(401)
        
        # make sure the user is authorized
        client_id = getUserID(flask.request.authorization.username, flask.request.authorization.password)

        if client_id == None:
            flask.abort(403)
        
        flask.g.client_id = client_id

        return f(*args, **kwargs)

    return wrap


#------------------------------------------------------
# Get a user's id from their email/password combination
#
# Parms:
#   email - user's email
#   password - user's password
# 
# Returns: 
#   user's id - (email/password combo was correct)
#   None - (INCORRECT email/password combo)
#------------------------------------------------------
def getUserID(email: str, password: str) -> int | None:
    db = DB()
    db.connect()

    cursor = db.getCursor(True)

    sql = 'SELECT u.id as id FROM Users u WHERE u.email = %s AND u.password = %s LIMIT 1'
    parms = (email, password)

    try:
        cursor.execute(sql, parms)
        rs: dict = cursor.fetchone()
        user_id = rs.get('id', None)
    except:
        user_id = None
    finally:
        db.close()

    return user_id   


#------------------------------------------------------
# Verify that the incoming request was made from the website
# and not some 3rd party rest service.
#
# Checks that the request has the custom header value.
#------------------------------------------------------
def no_external_requests(f):
    @wraps(f)
    def wrap(*args, **kwargs):        
        header_value = flask.request.headers.get(CLIENT_CUSTOM_HEADER_KEY, '', str)

        if header_value != keys.verification.header:
            flask.abort(403)

        return f(*args, **kwargs)

    return wrap