from config.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'virtual',
        'USER': 'postgres',
        'PASSWORD': 'virtual',
        "HOST": "db",
        "PORT": 5432,
    }
}
