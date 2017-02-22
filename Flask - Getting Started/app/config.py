# Web Forms with pip install Flask-WTF
WTF_CSRF_ENABLED = True
# Make sure this is hard to guess on live apps
SECRET_KEY = '0000'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]