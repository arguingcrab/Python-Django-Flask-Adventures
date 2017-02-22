# Routes
# - import the Flask class from the flask module
# - and {jinja2} html templates, providing template_name, and any vars
from flask import Flask, render_template

# - create the app obj
app = Flask(__name__)

# - use decorators to linkt he func() to a url
@app.route('/')
def home():
    return "Hello, World!"
    
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
    
# - start the server with 'run()'
if __name__ == '__main__':
    app.run(debug=True)