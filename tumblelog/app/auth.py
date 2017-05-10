from functools import wraps
from flask import request, Response, redirect, url_for
from flask_login import current_user

def check_auth(username, password):
    # check if username + password combination is valid
    return username == 'admin' and password == 'password'
    

def authenticate():
    # sends 401 response that enables basic auth
    return Response(
        ':( Bad credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )
    
    
# create a requires_auth decorator for basic auth
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # auth = request.authorization
        # if not auth or not check_auth(auth.username, auth.password):
        #     return authenticate()
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
    
def redirect_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated