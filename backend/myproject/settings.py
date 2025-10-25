from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# Log File Path
log_path = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_path, exist_ok=True)
LOG_FILE = os.path.join(log_path, 'backend.log')

SECRET_KEY = config('SECRET_KEY')

# DEBUG = True
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', f"{os.environ.get('EXPORT_HOST')}"]
CSRF_TRUSTED_ORIGINS = [
	f"http://localhost:{os.environ.get('EXPORT_PORT')}", f"http://127.0.0.1:{os.environ.get('EXPORT_PORT')}", 
	f"http://0.0.0.0:{os.environ.get('EXPORT_PORT')}", f"http://{os.environ.get('EXPORT_HOST')}:{os.environ.get('EXPORT_PORT')}",
	f"http://{os.environ.get('EXPORT_HOST')}:8282"
]

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
  	'rest_framework',
	'django_apscheduler',
	'tradeapp'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

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

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
	'default': {
		'ENGINE': 'django.contrib.gis.db.backends.mysql',
		# 'HOST': os.environ.get('DB_HOST'),
		'HOST': 'host.docker.internal',
		'NAME': os.environ.get('DB_NAME'), # DB명
		'USER': os.environ.get('DB_USER'), # 데이터베이스 계정
		'PASSWORD': os.environ.get('DB_PW'),
		'PORT': 3306, # 데이터베이스 포트(보통은 3306)
		'CONN_MAX_AGE': 60,
		'CONN_HEALTH_CHECKS': True,
		# 'OPTIONS': {
			# 'init_command' : "SET sql_mode='STRICT_TRANS_TABLES'",
			# 'connect_timeout': 60,
		# }
	}
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		}
	},
	'formatters': {
		'django.server': {
			'()': 'django.utils.log.ServerFormatter',
			'format': '[{server_time}] {message}',
			'style' : '{',
			
		},
		'standard': {
			'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
		}
	},
	'handlers': {
	   'console': {
			'level': 'INFO',
			'filters': ['require_debug_true'],
			'class': 'logging.StreamHandler',
			'formatter': 'standard',
		},
		'django.server': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'django.server',
		},
		'file': {
		  'level': 'DEBUG',
		  'filters': ['require_debug_false'],
		  'class': 'logging.handlers.TimedRotatingFileHandler',
		  'filename': LOG_FILE,
		  'when': "midnight",
		  'backupCount': 100,
		  'formatter': 'standard',
		}
	},
	'root': {
		'handlers': ['console'],
		'level': 'INFO',
	},
	'loggers': {
        'scheduler': {
			'handlers': ['console', 'file'],
			'level': 'INFO',
		},
		'django': {
			'handlers': ['console', 'file'],
			'level': 'INFO',
		},
		'tradeapp.views': {
			'handlers': ['console', 'file'],
			'level': 'INFO',
			'propagate': False
		},
		'tradeapp.views_scheduler': {
			'handlers': ['console', 'file'],
			'level': 'INFO',
			'propagate': False
		},
		'tradeapp.serializers': {
			'handlers': ['console', 'file'],
			'level': 'INFO',
			'propagate': False
		}
	}
}
