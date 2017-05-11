import os


LOCAL = 'local'
STAGING = 'staging'
PRODUCTION = 'production'

ENV = os.environ.get('FLASK_ENV', LOCAL)


from .common import *

if ENV == PRODUCTION:
    from .production import *
elif ENV == LOCAL:
    from .local import *
elif ENV == STAGING:
    from .staging import *