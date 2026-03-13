import os
import pymysql
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

# FINAL UNBREAKABLE PATCH - Hardcoded Fallbacks
SECRET_KEY = 'django-insecure-ti-prtjm(d_p7ve!r(g&4&(=+*_vn*x+*3z^ge567i72tr-5)1'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django_prometheus',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'corsheaders',
    'subway',   
    'stories',
    'library',
    'rest_framework',
    'storages',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SB_DB_NAME", "postgres"),
        "USER": os.getenv("SB_DB_USER", "postgres.jlvhwihvmivvihffhxse"),
        "PASSWORD": "hisubtory1234",
        "HOST": os.getenv("SB_DB_HOST", "aws-1-ap-northeast-2.pooler.supabase.com"),
        "PORT": os.getenv("SB_DB_PORT", "5432"),
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "hisubtory_db"),
        "USER": os.getenv("DB_USER", "admin"),
        "PASSWORD": "8gEEJTwfFTMRhRFIMNrF",
        "HOST": os.getenv("DB_HOST", "hisubtory-db.cnwkq8oe8jr5.ap-northeast-2.rds.amazonaws.com"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

DATABASE_ROUTERS = ['project.router.DatabaseRouter']
REDIS_HOST = os.getenv("REDIS_HOST", "hisubtory-redis.rkthpz.0001.apn2.cache.amazonaws.com")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"}
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
AUTH_USER_MODEL = 'accounts.User'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://hisubtory-alb-1990322498.ap-northeast-2.elb.amazonaws.com",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
