from pathlib import Path
from pathlib import Path

# /////////////////////////////////
from pathlib import Path
import os   
from datetime import datetime, timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x8-o&wz2asy$#%-#nk&dszbf$jkvp^-y9n%(yu_*+i2j+55(#r'

DEBUG = True
# DEBUG = False

ALLOWED_HOSTS = ['.vercel.app','now.sh','127.0.0.1','localhost','ec2-3-7-9-101.ap-south-1.compute.amazonaws.com','3.7.9.101']

# Application definition
    # 'jet.dashboard',

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    'django_nvd3',
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'accounts',    
    'social.apps.django_app.default',
    'rest_framework_simplejwt',    
    'rest_framework',    
]

# 'django_cleanup.apps.CleanupConfig',

    # 'multiupload',

X_FRAME_OPTIONS = 'SAMEORIGIN'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=600),
}

JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
# JET_INDEX_DASHBOARD = 'myapp.dashboard.CustomIndexDashboard'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'bulbulDrone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myapp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

WSGI_APPLICATION = 'bulbulDrone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': '2FFDAadg36cA642FBGF51BbcFaCG*Aef',
#         'HOST': 'roundhouse.proxy.rlwy.net',
#         'PORT': '38843',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'veertours',
#         'USER': 'root',
#         'PASSWORD': 'amazon@9881',
#         'HOST': 'localhost',  # You can use an IP address or 'localhost' if it's on the same machine
#         'PORT': '3306',  # Default MySQL port is 3306
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# DJANGO_BASE_PATH = '/djangoapp1/'
# STATIC_URL = '/djangoapp1/static/'
MEDIA_URL = '/djangoapp1/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATICFILES_DIRS = os.path.join(BASE_DIR, 'static'),
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')


#Add this at the bottom in settings.py
#social app custom settings 
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'accounts.CustomUser'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '452866610917-54pg2s8i7o5iuouc3hkllkvi0qja5jtf.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'oeJjAF1Umt8zJsqblS7cwa5X'

# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-client-id'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-client-secret'
# SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://localhost:8000/complete/google-oauth2/'
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI =[
    'http://127.0.0.1:8000/auth/complete/google-oauth2/',
    'http://127.0.0.1:8000/social-auth/complete/google-oauth2/',
    'https://drone-app-backend.vercel.app/auth/complete/google-oauth2/',
    'https://drone-app-backend.vercel.app/social-auth/complete/google-oauth2/'
    ]