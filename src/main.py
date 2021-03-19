import flask
from flask import Flask, jsonify, request, current_app, abort
from flask_cors import CORS
from functools import wraps, update_wrapper
from markupsafe import escape
from User import User
from Utilities import Utilities
from Login import Login



app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    
    return jsonify(request.authorization)
    # return jsonify(dict(request.headers))

    # return jsonify(request.headers.__dict__)
    # return ''

    # return 

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        new_user = User()

        # set the user properties
        new_user.email      = request.form['email']
        new_user.password   = request.form['password']
        new_user.name_first = request.form['name_first']
        new_user.name_last  = request.form['name_last']
        new_user.birth_date = request.form['birth_date']
        
        new_user.insert()
        new_user.fetch()

        return jsonify(new_user.__dict__)

    else:
        return 'sup'

@app.route('/users/<int:user_id>', methods=['GET'])
def user(user_id):
    if request.method == 'GET':
        user = User(id=user_id)
        user.fetch()
        return jsonify(user.__dict__)


@app.route('/login', methods=['GET'])
def login():
    userID = Login.isValidLoginAttempt(request.args['email'], request.args['password'])

    if userID == None:
        flask.abort(404)


    user = User(id=userID)
    user.fetch()
    return jsonify(user.__dict__)







