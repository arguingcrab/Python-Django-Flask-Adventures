from cerberus import Validator
from .bad_words import stops


# validator for .models Post.save schema = {}
class MyValidator(Validator):
    def _validate_filter_words(self, filter_word, field, value):
        for x in filter_word.split():
            if x.lower() in stops:
                self._error(field, 'Invalid word found in field <%s>:   "%s"' % (field, x))