"""
Django settings for UltraExperts project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import django_heroku
from .constants import *
import os
from datetime import datetime,timedelta
from elasticsearch import RequestsHttpConnection

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = SECRET_KEY
DEBUG = DEBUG
#ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io','UltraExperts.herokuapp.com','ultraxpert-frontend.herokuapp.com']

if DEBUG == False:
    SECURE_SSL_REDIRECT = True
else:
    SECURE_SSL_REDIRECT = False

if DEBUG==True:
    BASE_URL = BASE_URL
else:
    BASE_URL = os.environ["BASE_URL"]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'storages',
    'phonenumber_field',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'ckeditor',
    'drf_yasg',
    #elastic search
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
]

# social authenticaton application

INSTALLED_APPS+=[
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',

]

# SYSTEM APPLICATION

INSTALLED_APPS+=[
    'meet',
    "user",
    "activity",
    "chat",
    "events",
    "payment",
    "search"

]

ELASTICSEARCH_DSL = {
        "default":{
                    "hosts": ELASTIC_SEARCH_URL,
                    "http_auth": AWS_AUTH,
                    "use_ssl": True,
                    "verify_certs": True,
                    "connection_class": RequestsHttpConnection,
                    }
}
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'UltraExperts.urls'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["template"],
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

WSGI_APPLICATION = 'UltraExperts.wsgi.application'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["https://UltraExperts.herokuapp.com","http://localhost:3000","http://127.0.0.1:8000","https://ultraxpert-frontend.herokuapp.com",]
#CORS_ORIGIN_ALLOWED_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# server =  os.getenv("SERVER")
# if server == "TEST":
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'UltraXpert',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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

# authentication
AUTH_USER_MODEL = 'user.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = "username"
ACCOUNT_EMAIL_VARIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = "/user/user_plan_selection/"
OLD_PASSWORD_FIELD_ENABLED = True
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'jwt-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'
SITE_ID = 1

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'UltraExperts.serializers.UserSerilizer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'UltraExperts.authenticate.CustomAuthentication',
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=3600),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_COOKIE_HTTP_ONLY' : False,
    'AUTH_COOKIE_PATH': '/',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': False, 
    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}





#social auth

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
SOCIAL_AUTH_FACEBOOK_KEY = SOCIAL_AUTH_FACEBOOK_KEY
SOCIAL_AUTH_FACEBOOK_SECRET = SOCIAL_AUTH_FACEBOOK_SECRET
SOCIAL_AUTH_LOGIN_REDIRECT_URL = SOCIAL_AUTH_LOGIN_REDIRECT_URL
SOCIAL_AUTH_FACEBOOK_SCOPE = SOCIAL_AUTH_FACEBOOK_SCOPE
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS
SOCIAL_AUTH_USER_FIELDS = SOCIAL_AUTH_USER_FIELDS
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE =  SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE


  

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME =S3_BUCKET_NAME
MEDIA_URL = f'/http://%s.s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/media/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_DEFAULT_ACL = None
REGION_NAME = REGION_NAME

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# ckeditor configuration
ADMIN_SITE_HEADER = ADMIN_SITE_HEADER 

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

CKEDITOR_UPLOAD_PATH = '/upload/'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "onlinewebsitemarket@gmail.com"
EMAIL_HOST_PASSWORD = "weckbhyqcfcepjtn"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'UltraTeam Team <noreply@onlinewebsitemarket.com>'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

django_heroku.settings(locals())
