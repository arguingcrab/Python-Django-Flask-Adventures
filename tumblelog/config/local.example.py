from app import app
from mongoengine import connect
from flask_mongoengine import MongoEngine

SECRET_KEY = '0000'

# --- mLab MongoDB Deployments (new > single-node > aws-sandbox)
DB_NAME = 'db-name'
DB_USERNAME = 'user'
DB_PASSWORD = 'password'
DB_HOST_ADDRESS = 'address:port/db-name'


# app.config["MONGODB_DB"] = DB_NAME
MONGODB_DB = DB_NAME
connect(DB_NAME, host="mongodb://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST_ADDRESS)
