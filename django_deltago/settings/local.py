from .base import *

SECRET_KEY = 'i!5fb)i+-wq^ur*_0v3s%y+847u($jl#9$x&r-j+p475n#bb9t'
DEBUG = True

ALLOWED_HOSTS = [u'localhost', u'127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}