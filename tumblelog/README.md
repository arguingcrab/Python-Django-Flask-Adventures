# Writing a Tumblelog App with Flask && MongoEngine

[https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt](https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt)

using mLab 

[https://mlab.com](https://mlab.com)

validation with 

[http://docs.python-cerberus.org/en/stable/index.html](http://docs.python-cerberus.org/en/stable/index.html)

login and registration with

[https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)

design(s) with

[http://materializecss.com/](http://materializecss.com/)

[https://www.kryogenix.org/code/browser/sorttable/](https://www.kryogenix.org/code/browser/sorttable/)


### commands and console
`python manage.py runserver`

`python manage.py shell`
```
>>> from app.models import *
>>> from werkzeug.security import generate_password_hash
>>> user = User('admin', 'admin@example.com', generate_password_hash('password'), 'admin', True)
>>> user.save()
```


### todo
- [ ] add role --> user
- [ ] flask-security `pip install flask-security` for confirmation and reset
- [x] add search
  - [x] search category
  - [x] search posts
- [ ] wordfence-like/analytics/pingdom feature(s)
  - [x] basic session & login history
  - [x] logout specific user
  - [ ] identify country if not local
- [ ] change validation to be with mongoengine
- [x] manage comments
- [ ] redirects and 404s
- [ ] sort by archived and not
  - [ ] admin
  - [ ] front
- [ ] permissions
- [ ] edit post previews
  - [ ] video
  - [ ] image
- [ ] mass delete posts with confirmation
- [ ] func() for clearing session
  ```
  user = User.objects.get(username=current_user.username)
  session = Session.objects.get(user=user)
  session.update(set__session='')
  ```


### list / table view
```
# user (-password)
{
    "_id": "_id",
    "username": "username",
    "email": "email",
    "status": "status",
    "active": "active",
    "created_at": "created_at"
}
# post
{
    "_id": "_id",
    "_cls": "_cls",
    "created_at": "created_at",
    "title": "title",
    "slug": "slug",
    "post_author": "post_author",
    "body": "body",
    "author": "author",
    "embed_code": "embed_code",
    "image_url": "image_url"
}
# login_history
{
    "_id": "_id",
    "user": "user",
    "ip": "ip",
    "date_time": "date_time"
}

# session
{
    "_id": "_id",
    "user": "user",
    "ip": "ip",
    "session": "session",
    "last_login": "last_login"
}
```
