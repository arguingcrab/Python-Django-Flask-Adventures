from app import app
from flask import render_template, redirect, url_for, request, flash
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Aidi'}
    posts = [
        {'author': {'nickname': 'Esper'},
        'body': 'Lorem Ipsum',
        },
        {'author': {'nickname': 'Koko'},
        'body': 'Lorem Ipsum',
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
            (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])