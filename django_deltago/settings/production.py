from .base import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = bool(os.environ.get('DJANGO_DEBUG'))

ALLOWED_HOSTS = [u'deltago.ainesmile.com', u'172.104.73.110',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deltagodb',
        'USER': 'deltagouser',
        'PASSWORD': 'deltagopassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}