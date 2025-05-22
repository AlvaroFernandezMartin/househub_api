from pathlib import Path
import os
from corsheaders.defaults import default_headers
import cloudinary

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = 'django-insecure-amq4^6-exm5#n7jb41yfhi1!ou!^k@y#5_q+su$ks2mc(=(3p2'
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'househubapi-production.up.railway.app']

# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',

    # Local
    'users.apps.UsersConfig',
    'houses.apps.HousesConfig',
    'shared.apps.SharedConfig',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 🔥 Para servir archivos estáticos
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC & MEDIA
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'househub_api.urls'
WSGI_APPLICATION = 'househub_api.wsgi.application'

# DATABASE (usando SQLite local, cambiar a PostgreSQL si usas Railway DB)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# CORS CONFIGURATION
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "https://househubapi-production.up.railway.app"
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.railway\.app$",
    r"^http://127\.0\.0\.1:8080$",
]
CORS_ALLOW_HEADERS = list(default_headers) + ['content-type']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']

# CLOUDINARY CONFIG
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name='dxinpqg5y',
    api_key='284688185574276',
    api_secret='0xisMtgoNdKqtiSxu9GzqRA5dtc',
    secure=True
)

# USE HTTPS HEADERS WHEN DEPLOYED IN PROXIED ENVIRONMENTS LIKE RAILWAY
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
