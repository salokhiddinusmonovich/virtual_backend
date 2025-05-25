from config.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'virtual',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        "HOST": "db",
        "PORT": 5432,
    }
}
