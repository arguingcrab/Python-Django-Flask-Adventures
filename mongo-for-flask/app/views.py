from flask import Flask, render_template, send_from_directory
from app import app

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
    
@app.route('/')
def index():
    return render_template('index.html')
    
    
def get_user_from_db(facebook_id):
    if not facebook_id:
        raise ValueError()
    users_found = User.objects(facebook_id=facebook_id)
    if len(users_found) == 1:
        return users_found[0]
    elif len(users_found) == 0:
        return None
    else:
        raise Exception('Database Integrity Error')