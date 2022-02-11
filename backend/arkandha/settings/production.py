from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres', 
        'PASSWORD': 'postgres',
        'HOST': 'db_postgres', 
        'PORT': 5432,
    }
}