import app, os
from mongoengine import connect
from flask_mongoengine import MongoEngine

SECRET_KEY = os.environ.get('SECRET_KEY')

# --- mLab MongoDB Deployments (new > single-node > aws-sandbox)
DB_NAME = os.environ.get('DB_NAME')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST_ADDRESS = os.environ.get('DB_HOST_ADDRESS')


# app.config["MONGODB_DB"] = DB_NAME
MONGODB_DB = DB_NAME
connect(DB_NAME, host="mongodb://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST_ADDRESS)