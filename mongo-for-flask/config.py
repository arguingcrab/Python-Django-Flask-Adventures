from app import app
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

SECRET_KEY = '0000'

# --- mLab MongoDB Deployments (new > single-node > aws-sandbox)
DB_NAME = 'ac-test'
DB_USERNAME = 'root'
DB_PASSWORD = 'roottoor'
DB_HOST_ADDRESS = 'ds131621.mlab.com:31621/ac-test'


app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host="mongodb://" + DB_USERNAME + ":" + DB_PASSWORD + "@" + DB_HOST_ADDRESS)
