# Routing
[Quickstart](http://flask.pocoo.org/docs/0.12/quickstart/)

## Examples for route()

```python
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'
```

## Examples for route() with variables

```python
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
```

Converters

| Type        | Accepts           |
| ------------- |:-------------:|
| string      | accepts text without slash (default) |
| int      | accepts int |
| float      | accepts float |
| path      | accepts text with slash |
| any      | matches one of the items provided |
| valid      | accepts UUID str |

## Unique URLs and Behaviour
```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```
- first will add a trailing slash if you access it without
- second will display a 404 if accessed with a trailing /

## URL Building
Flask can build a url with url_for()
test_request_context() tells Flask to behave as though it is handling a request while interacting with shell
```python
  from flask import Flask, url_for
  app = Flask(__name__)
  @app.route('/')
  def index(): pass

  @app.route('/login')
  def login(): pass

  @app.route('/user/<username>')
  def profile(username): pass

  with app.test_request_context():
    print url_for('index')
    print url_for('login')
    print url_for('login', next='/')
    print url_for('profile', username='John Doe')
```
- /
- /login
- /login?next=/
- /user/John%20Doe

## HTTP Methods
[Full](http://flask.pocoo.org/docs/0.12/quickstart/#http-methods)

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()
```