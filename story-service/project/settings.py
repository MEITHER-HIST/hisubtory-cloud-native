import os
import pymysql
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-emergency-force-key-fixed-12345")
DEBUG = True
ALLOWED_HOSTS = ['*']

# 세션 쿠키 설정 통일
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'hisubtory_sessionid')
SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

INSTALLED_APPS = [
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
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SB_DB_NAME", "postgres"),
        "USER": os.getenv("SB_DB_USER", "postgres"),
        "PASSWORD": os.getenv("SB_DB_PASSWORD", "hisubtory1234"),
        "HOST": os.getenv("SB_DB_HOST", "db-postgres"),
        "PORT": os.getenv("SB_DB_PORT", "5432"),
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "hisubtory_db"),
        "USER": os.getenv("DB_USER", "admin"),
        "PASSWORD": os.getenv("DB_PASSWORD", "mysql_password"),
        "HOST": os.getenv("DB_HOST", "db-mysql"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

DATABASE_ROUTERS = ['project.router.DatabaseRouter']
AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
