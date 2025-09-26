
import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-secret-key'
DEBUG = False
ALLOWED_HOSTS = [
    # Add your Render domain here
    'vsc-repo.onrender.com', 
    # Add your custom domain if you have one
    # You may also want to include the localhost for development:
    '127.0.0.1', 
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rooms',
    'students',
    'rest_framework',
    'hostel_management',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
]


ROOT_URLCONF = 'hostel_management.urls'
LOGIN_URL = '/students/login/'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
    ]},
}]
import os
# ...
SECRET_KEY = os.environ.get('SECRET_KEY') # If this returns None, it fails
# OR
# hostel_management/settings.py

# TEMPORARY FIX: REPLACE THIS WITH YOUR ACTUAL SECRET_KEY from development
# AND ADD IT TO RENDER'S ENVIRONMENT VARIABLES ASAP
SECRET_KEY = 'django-insecure-your-secret-key-from-local-settings' 
# ... and remove any os.environ lookup for it
# SECRET_KEY = os.environ['SECRET_KEY'] # If SECRET_KEY is missing, this causes the error immediately
WSGI_APPLICATION = 'hostel_management.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Directory where collectstatic will collect static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
LOGIN_URL = '/students/login/'
LOGIN_REDIRECT_URL = '/students/dashboard/'
