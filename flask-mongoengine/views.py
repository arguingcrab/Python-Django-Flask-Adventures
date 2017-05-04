# 404 if obj !exists
def view_todo(todo_id):
    todo = Todo.objects.get_or_404(_id=todo_id)
# ...

# Paginate
def view_todos(page=1):
    paginated_todos = Todo.objects.paginate(page=page, per_page=10)
    
# Paginate through tags
def view_todo_tags(todo_id, page=1):
    todo = Todo.objects.get_or_404(_id=todo_id)
    paginated_tags = todo.paginate_field('tags', page, per_page=10)