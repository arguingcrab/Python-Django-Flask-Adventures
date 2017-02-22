# Routes
# - import the Flask class from the flask module
# - and {jinja2} html templates, providing template_name, and any vars
# Login - import request, redirect, url_for
from flask import Flask, render_template, redirect, url_for, request

# - create the app obj
app = Flask(__name__)

# - use decorators to linkt he func() to a url
@app.route('/')
def home():
    return "Hello, World!"
    
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# Login - add route for handling login request/logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid Credentials. Please Try Again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
# - start the server with 'run()'
if __name__ == '__main__':
    app.run(debug=True)