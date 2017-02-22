from flask import Flask

app = Flask(__name__)
# import config.py
app.config.from_object('config')
from app import views