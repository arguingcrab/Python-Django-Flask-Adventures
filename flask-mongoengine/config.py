import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True

app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': 'localhost',
    'port': 27017,
    # 'username': '',
    # 'password': '',
}

# mongodb individually
# app.config['MONGODB_DB'] = 'test'
# app.config['MONGODB_HOST'] = 'localhost'
# app.config['MONGODB_USERNAME'] = 'user'
# app.config['MONGODB_PASSWORD'] = 'password'

# flask debug panel
app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']