from flask import Blueprint

test = Blueprint('test', __name__)

@test.route('/')
def index():
    return "Test blueprint"

