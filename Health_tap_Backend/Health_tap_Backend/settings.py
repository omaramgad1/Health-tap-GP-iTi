
import dj_database_url
from pathlib import Path
import environ
from datetime import timedelta
from .jazmin import JAZZMIN_SETTINGS
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


## Environment variables ##
env = environ.Env()
environ.Env.read_env()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRECT')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    #####################
    'jazzmin',
    #####################
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #####################
    'drf_yasg',
    'rest_framework',
    "phonenumber_field",
    'cloudinary',
    'cloudinary_storage',
    'corsheaders',
    'django_filters',
    #######################
    'Specialization',
    'User',
    'Doctor',
    'Patient',
    'City',
    'District',
    'Appointment',
    'Reservation',
    'MedicalEntry',
    'Review',
    'MedicalCode',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Health_tap_Backend.urls'

### JWT Authorization Settings ###
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    # "Bearer <Token>"
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

STRIP_SECRETE_KEY = 'sk_test_51N6ijoDIajLiykdANbBTjryP0yU2fqkf3Ta8vB4LepConqUjHImukXhzXsFFTgs0iOTmH9BSZb7Y25mMTT59oysA00UfbdvZGQ'

WSGI_APPLICATION = 'Health_tap_Backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database postgresql Local
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME_LOCAL'),
        'USER': env('USER_LOCAL_DB'),
        'PASSWORD': env('PASSWORD_LOCAL_DB'),
        'HOST': env('HOST_LOCAL_DB'),
        'PORT': env('PORT_LOCAL_DB'),
    }
}


# Render postgresql live database

# DATABASES = {
#     'default': dj_database_url.parse(env('DATABASE_URL'))
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

cloudinary.config(
    cloud_name=env('CLOUD_NAME'),
    api_key=env('API_KEY'),
    api_secret=env('API_SECRET'),


)


# Cloudinary settings
# MEDIA_URL = '/media/'
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': env('CLOUD_NAME'),
#     'API_KEY': env('API_KEY'),
#     'API_SECRET': env('API_SECRET'),
# }


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#### CORS settings###
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    # 'http://localhost:3000',
    # 'https://main--jassafashion.netlify.app/'
]


#### REST Settings ###
REST_FRAMEWORK = {
    # "NON_FIELD_ERRORS_KEY": "errors",
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    
}

#### Custom User Model #####
AUTH_USER_MODEL = "User.user"


# STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
# STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

JAZZMIN_SETTINGS = JAZZMIN_SETTINGS

SITE_URL = 'http://localhost:3000'