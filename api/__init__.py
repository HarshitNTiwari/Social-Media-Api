from flask import Flask
from flask_jwt import JWT

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dv38t4gb28iv8'
app.config['JWT_AUTH_URL_RULE'] = '/api/authenticate'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

from api import routes