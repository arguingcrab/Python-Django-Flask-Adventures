from functools import wraps
from flask import request, Response, redirect, url_for
from flask_login import current_user, login_required
from app import login_manager

"""
authentication decorators
"""


# redirects if authenticated (ex: login)    
def redirect_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        return f(*args, **kwargs)
    return decorated
    

# redirect if not authenticated, then redirect to where they wanted to go    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
    
