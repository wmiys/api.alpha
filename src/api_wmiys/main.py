from flask import Flask
from api_wmiys.test.controllers import test

app = Flask(__name__)
app.register_blueprint(test, url_prefix='/test')