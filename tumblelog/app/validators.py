from cerberus import Validator
from .b import stops

class MyValidator(Validator):
    def _validate_filter_words(self, filter_word, field, value):
        for x in filter_word.split():
            if x.lower() in stops:
                self._error(field, 'Invalid word found in field <%s>:   "%s"' % (field, x))