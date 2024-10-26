# config/test_settings.py

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_commerce1_db_test',
        'USER': 'style_user1',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}