from blinker import Namespace
from .b import stops
test = Namespace()

post_pre_save = test.signal('pre-save')
# @classmethod
def pre_save(cls, sender, document, **kwargs):
    error = None
    for x in document.title.split():
        if x.lower() in stops:
            error = x.lower()
    return error
    
post_pre_save.connect(pre_save)