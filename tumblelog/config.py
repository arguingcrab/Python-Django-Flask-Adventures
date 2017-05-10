from app import app
from mongoengine import connect
from flask_mongoengine import MongoEngine

SECRET_KEY = '0000'

# --- mLab MongoDB Deployments (new > single-node > aws-sandbox)
# DB_NAME = 'database'
# DB_USERNAME = 'username'
# DB_PASSWORD = 'password'
# DB_HOST_ADDRESS = 'address:0000'
# 
# 
# # app.config["MONGODB_DB"] = DB_NAME
# MONGODB_DB = DB_NAME
# connect(DB_NAME, host="mongodb://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST_ADDRESS)
