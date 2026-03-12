import os
import pymysql
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-emergency-force-key-fixed-999")
DEBUG = True
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ["http://hisubtory-alb-1990322498.ap-northeast-2.elb.amazonaws.com", 
    "http://hisubtory-alb-1990322498.ap-northeast-2.elb.amazonaws.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOWED_ORIGINS = [
    "http://hisubtory-alb-1990322498.ap-northeast-2.elb.amazonaws.com",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'corsheaders',
    'rest_framework',
    'pages',
    'subway',
    'stories',
    'library',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SB_DB_NAME", "postgres"),
        "USER": os.getenv("SB_DB_USER", "postgres"),
        "PASSWORD": (os.getenv("SB_DB_PASSWORD") or "hisubtory1234"),
        "HOST": os.getenv("SB_DB_HOST", "aws-1-ap-northeast-2.pooler.supabase.com"),
        "PORT": os.getenv("SB_DB_PORT", "5432"),
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "hisubtory_db"),
        "USER": os.getenv("DB_USER", "admin"),
        "PASSWORD": os.getenv("DB_PASSWORD", "mysql_password"),
        "HOST": os.getenv("DB_HOST", "hisubtory-db.cnwkq8oe8jr5.ap-northeast-2.rds.amazonaws.com"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}

DATABASE_ROUTERS = ['project.router.DatabaseRouter']

CORS_ALLOW_ALL_ORIGINS = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

# 세션 쿠키 설정 통일
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'hisubtory_sessionid')
SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Redis Cache 설정
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = os.getenv("REDIS_URL", f"redis://{REDIS_HOST}:{REDIS_PORT}/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# 세션 저장 설정
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
