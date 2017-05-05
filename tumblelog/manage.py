import os, sys
from flask_script import Manager, Server
from app import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# basedir = os.path.abspath(os.path.dirname(__file__))

manager = Manager(app)

# turn on debugger by default & reloader
manager.add_command("runserver", Server(
    use_debugger = True, 
    use_reloader = True, 
    host = 'localhost'
))

if __name__ == "__main__":
    manager.run()