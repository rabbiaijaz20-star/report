import os
from pathlib import Path
from dotenv import load_dotenv

# ===========================
# BASE DIRECTORY
# ===========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===========================
# LOAD ENVIRONMENT VARIABLES
# ===========================
load_dotenv()  # loads .env if it exists

# ===========================
# SECURITY SETTINGS
# ===========================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-dev-key')  # fallback for local dev
DEBUG = False
ALLOWED_HOSTS = ['*']

# ===========================
# INSTALLED APPS
# ===========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your app
    'report',
]

# ===========================
# MIDDLEWARE
# ===========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===========================
# URL CONFIGURATION
# ===========================
ROOT_URLCONF = 'stagereport.urls'

# ===========================
# TEMPLATES
# ===========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # This points to C:\Users\Mega Computers\report\stagereport\templates
        'DIRS': [BASE_DIR / 'stagereport' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by auth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===========================
# WSGI
# ===========================
WSGI_APPLICATION = 'stagereport.wsgi.application'

# ===========================
# DATABASE
# ===========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===========================
# PASSWORD VALIDATION
# ===========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===========================
# INTERNATIONALIZATION
# ===========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ===========================
# STATIC FILES
# ===========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ===========================
# MEDIA FILES
# ===========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===========================
# DEFAULT PRIMARY KEY FIELD TYPE
# ===========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===========================
# LOGIN / LOGOUT REDIRECTS
# ===========================
LOGIN_URL = 'report:login'
LOGIN_REDIRECT_URL = 'report:dashboard'
LOGOUT_REDIRECT_URL = 'report:login'

# ===========================
# EMAIL BACKEND (development)
# ===========================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'