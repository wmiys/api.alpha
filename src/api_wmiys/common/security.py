import flask
from flask import request
from functools import wraps
from wmiys_common import keys
from ..db import DB
from .globals import Globals

# setup the global variables container
requestGlobals = Globals(client_id=None)


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
        if not request.authorization:
            flask.abort(401)
        
        # make sure the user is authorized
        clientID = getUserID(request.authorization.username, request.authorization.password)
        if clientID == None:
            flask.abort(401)
        
        global requestGlobals
        requestGlobals.client_id = clientID

        # finally call f. f() now haves access to g.user
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
def getUserID(email: str, password: str):
    db = DB()
    db.connect()

    cursor = db.getCursor(True)

    sql = 'SELECT u.id as id FROM Users u WHERE u.email = %s AND u.password = %s LIMIT 1'
    parms = (email, password)

    try:
        cursor.execute(sql, parms)
        record_set: dict = cursor.fetchone()
        result = record_set.get('id', None)
    except:
        result = None
    finally:
        db.close()

    return result   


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

        if header_value != keys.client_verification.header:
            flask.abort(403)

        # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)

    return wrap