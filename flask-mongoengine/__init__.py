from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension

# setting up db before app init
# db = MongoEngine()

app = Flask(__name__, instance_relative_config = True)
app.config.from_pyfile('config.py')
db = MongoEngine(app)

# MongoEngine as session store - session interface config
app.session_interface = MongoEngineSessionInterface(db)

# debug panel
toolbar = DebugToolbarExtension(app)

# db.init_app(app)