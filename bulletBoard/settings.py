import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # добавленные приложения
    'ads.apps.AdsConfig', 'sign',

    # добавленные библиотеки
    'django.contrib.flatpages',
    'django.contrib.sites',
    'allauth', 'allauth.account',

    # crispy
    'crispy_forms',

    # WYSIWYG-редактор
    'ckeditor',
    'ckeditor_uploader',  # работа с медиафайлами

    'django_celery_beat',  # Для рассылок
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Добавленные middleware
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',

]

ROOT_URLCONF = 'bulletBoard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Обязательное подтверждение email
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

WSGI_APPLICATION = 'bulletBoard.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# добавки для рассылки почты
EMAIL_HOST = 'smtp.yandex.ru'  # ажрес сервера яндекс почты
EMAIL_PORT = 465  # ПОРТ smtp серврера
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True  # ЯНДЕКС ИСПОЛЬЗУЕТ SSL, ПОЭТОМУ НУЖНО УСТАНАВЛИВАТЬ True
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # реальная отправка на почту
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'  # симуляция отправки для разработки

LOGIN_URL = '/sign/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_FORMS = {'signup': 'sign.models.UserRegisterForm'}

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки редактора текста со встроенным медиаконтентом
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
    'filebrowserUploadUrl': '/ckeditor/upload/',

    # Настройка для разрешения работы с картинками и видео
    'extraAllowedContent': ['iframe[*]', 'img[*]']
}

CKEDITOR_UPLOAD_PATH = 'uploads/'

# Настройки фильтрации контента, вводимого через Ck_Editor
BLEACH_ALLOWED_TAGS = [
    'div', 'nav', 'p', 'strong', 'em',
    'u', 's', 'br', 'b', 'i',
    'ul', 'ol', 'li', 'span',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'sub', 'sup',
    'a', 'img', 'blockquote'
]

BLEACH_ALLOWED_ATTRIBUTES = {
    '*': ['style', 'class'],
    'a': ['href', 'title', 'target'],
    'img': ['src', 'alt']
}

BLEACH_ALLOWED_STYLES = [
    'color', 'font-size', 'text-align',
    'width', 'height', 'background', 'background-color',
    'background-image', 'padding'
]


# Настройка redis-кэширования
REDIS_LOCATION = os.getenv('REDIS_LOCATION')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': 'bulletboard',
        }
    }
}

CELERY_BROKER_URL = os.getenv('REDIS_LOCATION')
CELERY_RESULT_BACKEND = os.getenv('REDIS_LOCATION')

# Код, чтобы стать менеджером
MANAGER_CODE = os.getenv('MANAGER_CODE')
