# Writing a Tumblelog App with Flask && MongoEngine

[https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt](https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt)

using mLab 
[https://mlab.com](https://mlab.com)

validation with 
[http://docs.python-cerberus.org/en/stable/index.html](http://docs.python-cerberus.org/en/stable/index.html)

login and registration with
[https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)

### commands and console
`python manage.py runserver`

`python manage.py shell`
```
>>> from app.models import *
>>> from werkzeug.security import generate_password_hash
>>> user = User('admin', 'admin@example.com', generate_password_hash('password'), 'admin', True)
>>> user.save()
```