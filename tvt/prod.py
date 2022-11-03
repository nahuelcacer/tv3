from .settings import *


DEBUG = True

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com','https://*.127.0.0.1']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd71mq6o5tmbp67',
        'USER': 'pevuijzbdjpxcn',
        'PASSWORD': '5b940043c12dae02d03fd2bc14c7e891a5cf6d311611692cdb634079988ff5db',
        'HOST': 'ec2-34-227-120-79.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

import django_heroku
django_heroku.settings(locals())