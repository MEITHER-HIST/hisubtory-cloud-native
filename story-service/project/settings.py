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

# 세션 쿠키 설정 통일
SESSION_COOKIE_NAME = os.getenv('SESSION_COOKIE_NAME', 'hisubtory_sessionid')
SESSION_COOKIE_DOMAIN = os.getenv('SESSION_COOKIE_DOMAIN', None)
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

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

# AWS S3 Settings
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-2")
AWS_S3_CUSTOM_DOMAIN = os.getenv("AWS_S3_CUSTOM_DOMAIN", "")

# 세션 공유 설정
SESSION_COOKIE_NAME = 'hisubtory_sessionid'
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Redis Cache 설정
REDIS_HOST = os.getenv("REDIS_HOST", "db-mysql") # default or get from env
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PROTOCOL = os.getenv("REDIS_PROTOCOL", "redis")
REDIS_URL = f"{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/0"

REDIS_OPTIONS = {
    "CLIENT_CLASS": "django_redis.client.DefaultClient",
    "SOCKET_CONNECT_TIMEOUT": 5,
    "SOCKET_TIMEOUT": 5,
}

if REDIS_PROTOCOL == "rediss":
    REDIS_OPTIONS["CONNECTION_POOL_KWARGS"] = {
        "ssl_cert_reqs": None
    }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": REDIS_OPTIONS,
    }
}

# 세션 저장 설정
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
