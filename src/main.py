from flask import Flask
from flask import jsonify
from flask import request
from markupsafe import escape
from User import User
from Utilities import Utilities
app = Flask(__name__)

@app.route('/')
def home():
    return 'home page'

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
