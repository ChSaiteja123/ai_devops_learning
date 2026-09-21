"""
Base settings for AI-Powered DevOps & Cloud Architecture Learning Platform.

LEVEL 1 LEARNING — Django Settings Explained:
----------------------------------------------
Settings files control every aspect of your Django project.
Django reads these to know:
  - Which apps are installed
  - How to connect to the database
  - Where to find templates and static files
  - How to handle authentication
  - And much more

We split settings into base / development / production to follow
the 12-Factor App methodology (https://12factor.net/)
"""
import os
from pathlib import Path

# BASE_DIR points to the project root (3 levels up from this file)
# Path(__file__) = config/settings/base.py
# .parent       = config/settings/
# .parent.parent = config/
# .parent.parent.parent = project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────
# SECRET_KEY is used for cryptographic signing. NEVER commit the real value.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-me-in-production-use-env-var')

# DEBUG = False in production. Never run DEBUG=True on a public server.
DEBUG = False

# Hosts that are allowed to serve this application
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# ─────────────────────────────────────────────
# INSTALLED APPS
# ─────────────────────────────────────────────
# Django ships with many built-in apps. We also add third-party and our own apps.
DJANGO_APPS = [
    'django.contrib.admin',           # Admin interface
    'django.contrib.auth',            # Authentication framework
    'django.contrib.contenttypes',    # Content type framework
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Static file management
]

THIRD_PARTY_APPS = [
    'rest_framework',             # Django REST Framework — builds REST APIs
    'rest_framework_simplejwt',   # JWT authentication tokens
    'corsheaders',                # Cross-Origin Resource Sharing
]

# django-filter is optional — include it only when installed
try:
    import django_filters  # noqa: F401
    THIRD_PARTY_APPS += ['django_filters']
except ImportError:
    pass

LOCAL_APPS = [
    'apps.accounts',      # User management & authentication
    'apps.courses',       # Course catalog
    'apps.lessons',       # Individual lessons within courses
    'apps.labs',          # Hands-on labs
    'apps.projects',      # Project-based learning
    'apps.architecture',  # Architecture diagram generator
    'apps.quizzes',       # Quiz system
    'apps.progress',      # Learning progress tracking
    'apps.ai_assistant',  # AI-powered chat assistant
    'apps.rag',           # RAG (Retrieval Augmented Generation)
    'apps.aiops',         # AIOps incident analyzer
    'apps.monitoring',    # Prometheus metrics & observability
    'apps.deployments',   # Deployment tracking
    'apps.notifications', # User notifications
    'apps.audit',         # Audit logging
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ─────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────
# Middleware is a layer of code that processes every request/response.
# Order matters — each middleware wraps the next.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Security headers
    # WhiteNoise serves static files efficiently — used when installed
    # (omitted gracefully if whitenoise is not in the environment)
    'django.contrib.sessions.middleware.SessionMiddleware',   # Session support
    'corsheaders.middleware.CorsMiddleware',                  # CORS headers
    'django.middleware.common.CommonMiddleware',              # URL normalization
    'django.middleware.csrf.CsrfViewMiddleware',              # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Attach user to request
    'django.contrib.messages.middleware.MessageMiddleware',   # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Clickjacking protection
    'apps.audit.middleware.AuditMiddleware',                  # Custom audit logging
]

# Insert WhiteNoise middleware right after SecurityMiddleware when available
try:
    import whitenoise  # noqa: F401
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
except ImportError:
    pass

ROOT_URLCONF = 'config.urls'

# ─────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Look for templates in /templates/
        'APP_DIRS': True,                   # Also look in each app's templates/ folder
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

WSGI_APPLICATION = 'config.wsgi.application'

# ─────────────────────────────────────────────
# DATABASE
# ─────────────────────────────────────────────
# For local development we allow a SQLite fallback when the PostgreSQL driver is
# unavailable or when the developer explicitly selects SQLite. This keeps the app
# runnable in environments such as Windows workstations without PostgreSQL.
try:
    import psycopg  # noqa: F401
    PSYCOPG_AVAILABLE = True
except ImportError:
    try:
        import psycopg2  # noqa: F401
        PSYCOPG_AVAILABLE = True
    except ImportError:
        PSYCOPG_AVAILABLE = False

USE_SQLITE = os.environ.get('USE_SQLITE', '').strip().lower() in {'1', 'true', 'yes', 'on'}

if USE_SQLITE or not PSYCOPG_AVAILABLE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'devops_platform'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'CONN_MAX_AGE': 60,  # Keep DB connections alive for 60 seconds
        }
    }

# ─────────────────────────────────────────────
# AUTHENTICATION
# ─────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.User'  # Our custom user model

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# ─────────────────────────────────────────────
# DJANGO REST FRAMEWORK
# ─────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # For browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # Browsable API in dev
    ],
}

# Add DjangoFilterBackend only when django-filter is installed
try:
    import django_filters  # noqa: F401
    REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'].insert(
        0, 'django_filters.rest_framework.DjangoFilterBackend'
    )
except ImportError:
    pass

# JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}

# ─────────────────────────────────────────────
# CELERY (Async Task Queue)
# ─────────────────────────────────────────────
# Celery lets Django offload long-running tasks (email, AI calls) to background workers.
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # 5 minutes max per task

# ─────────────────────────────────────────────
# REDIS CACHE
# ─────────────────────────────────────────────
# Use Redis when the package is installed; fall back to in-process memory cache
# so the app still starts in environments where Redis isn't available yet.
try:
    import redis  # noqa: F401
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL', 'redis://localhost:6379/2'),
        }
    }
except ImportError:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ─────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# STATIC FILES (CSS, JavaScript, Images)
# ─────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Django 4.2+ uses the STORAGES dict instead of STATICFILES_STORAGE /
# DEFAULT_FILE_STORAGE. WhiteNoise is used for static files when installed;
# fall back to the built-in ManifestStaticFilesStorage if it isn't.
try:
    import whitenoise  # noqa: F401
    _staticfiles_backend = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
except ImportError:
    _staticfiles_backend = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': _staticfiles_backend,
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─────────────────────────────────────────────
# AI / OPENAI
# ─────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o')
OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small'

# ─────────────────────────────────────────────
# CORS
# ─────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')

# ─────────────────────────────────────────────
# EMAIL
# ─────────────────────────────────────────────
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@devopsplatform.com')

# ─────────────────────────────────────────────
# OPENTELEMETRY
# ─────────────────────────────────────────────
OTEL_SERVICE_NAME = 'devops-learning-platform'
OTEL_EXPORTER_OTLP_ENDPOINT = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4317')

# ─────────────────────────────────────────────
# PLATFORM-SPECIFIC SETTINGS
# ─────────────────────────────────────────────
# Maximum file size for RAG document uploads (10 MB)
RAG_MAX_UPLOAD_SIZE_MB = 10
# Chunk size for document splitting
RAG_CHUNK_SIZE = 1000
RAG_CHUNK_OVERLAP = 200
# Vector store path
CHROMA_PERSIST_DIRECTORY = str(BASE_DIR / 'chroma_db')

# AIOps confidence threshold for auto-remediation suggestions
AIOPS_CONFIDENCE_THRESHOLD = 0.85
