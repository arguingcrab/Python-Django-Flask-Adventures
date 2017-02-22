from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
    
# 1. Import Flask

# 2. Create an instance of Flask - first arg is the name of the app's mod/package
# For a single mod, use __name__ because depending on if it's started as an app
# or impoted as a mod, the name will be different 
# ('__main__' v the actual import name
# Need so Flask knows where to look for templates, statics, etc

# 3. We use route() decorator to tell Flask what URL should trigger our func()

# 4. Func() is given a name which is also used to general URLs for that func()
# and returns the message we want to display in the user's browser

# 5. Run with 
# $ export FLASK_APP=hello.py
# $ flask run
# * Running on 127.0.0.1:5000 (localhost:5000)