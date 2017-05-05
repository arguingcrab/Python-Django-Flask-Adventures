from functools import wraps
from flask import request, Response

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
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated