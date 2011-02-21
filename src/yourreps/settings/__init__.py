import os.path
import socket

PROJECT_DIR = os.path.join(os.path.dirname(__file__), '..')
HOSTNAME = socket.gethostname().lower().split('.')[0].replace('-', '')

DEBUG = False
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Paul Smith', 'paulsmith@pobox.com'),
)
MANAGERS = ADMINS
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'yourreps',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, '..', '..', 'static'),
]
SECRET_KEY = '-4f-ruxiz0el(x1(y!0&o6yfcrgt8!spb(#w(jo7k(65d0#_&d'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
ROOT_URLCONF = 'yourreps.urls'
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'staticfiles.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.admin',
    'yourreps',
    'staticfiles',
)

try:
    exec "from yourreps.settings.host_%s import *" % HOSTNAME
except ImportError:
    pass

try:
    from yourreps.settings.local import *
except ImportError:
    pass
