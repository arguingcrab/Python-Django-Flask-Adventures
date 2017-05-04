from flask_mongoengine.wtf import model_form

# flask-mongoengine auto generates wtforms from MongoEngine models
class User(db.Document):
    email = db.StringField(required=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    
    
class Content(db.EmbeddedDocument):
    text = db.StringField()
    lang = db.StringField(max_length=3)
    
    
class Post(db.Document):
    title = db.StringField(max_length=120, required=True, validators=[
                    validators.InputRequired(message=u'Missing title.'),
                ])
    author = db.Reference(User)
    tags = db.ListField(db.StringField(max_length=30))
    content = db.EmbeddedDocument(Content)
    

PostForm = model_form(Post, field_args={'title': {'textarea': True}})


def add_post(request):
    form = PostForm(request.POST)
    if request.method == 'POST' and form.validate():
        # ...
        redirect('done')
    return render_template('add_post.html', form=form)