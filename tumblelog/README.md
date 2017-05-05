# Writing a Tumblelog App with Flask && MongoEngine

[https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt](https://github.com/danilobellini/docs-mongodb/blob/master/source/tutorial/write-a-tumblelog-application-with-flask-mongoengine.txt)


### commands and console
`python manage.py runserver`

`python manage.py shell`
```
>>> from app.models import *
>>> post = Post(title="Hello",slug="hello",body="Hello World!")
>>> post.save()
>>> comment = Comment(author="Aidi", body="Hi")
>>> post.comments.append(comment)
>>> post.save()
```