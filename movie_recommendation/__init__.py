from flask import Flask
import os

app = Flask(__name__)
secret_key = os.urandom(12).hex()
app.config['SECRET_KEY'] = secret_key
from movie_recommendation import routes
