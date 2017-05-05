from flask import Flask
from flask_mongoengine import MongoEngine

# sensitive data would go under /instance/config.py (from_pyfile)
app = Flask(__name__, instance_relative_config = True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

db = MongoEngine(app)

# register blueprint
def register_blueprints(app):
    # prevents circular imports
    from app.views import posts
    from app.admin import admin
    app.register_blueprint(posts)
    app.register_blueprint(admin)

register_blueprints(app)

if __name__ == '__main__':
    app.run()