import os
import re
from pathlib import Path
import dj_database_url
import cloudinary

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent

# CHAVE DE SEGURANÇA
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sua-chave-secreta-aqui')

# DEBUG: controlado por variável de ambiente (padrão True para não quebrar o comportamento atual)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# APPS INSTALADOS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Cloudinary para armazenamento de mídia (fotos enviadas)
    'cloudinary_storage',
    'cloudinary',
    
    # Ordenação por arrastar e soltar no Admin
    'adminsortable2',
    
    # App do projeto
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'
WSGI_APPLICATION = 'setup.wsgi.application'

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

# BANCO DE DADOS (Usa PostgreSQL no Render e SQLite localmente)
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# VALIDAÇÃO DE SENHAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# IDIOMA E FUSO HORÁRIO
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ARQUIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ARQUIVOS DE MÍDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CONFIGURAÇÃO E EXTRAÇÃO DO CLOUDINARY
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL', '').strip()
USE_CLOUDINARY = bool(CLOUDINARY_URL) or bool(os.environ.get('CLOUDINARY_CLOUD_NAME'))

if CLOUDINARY_URL:
    match = re.match(r'cloudinary://([^:]+):([^@]+)@(.+)', CLOUDINARY_URL)
    if match:
        api_key, api_secret, cloud_name = match.groups()
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': cloud_name,
            'API_KEY': api_key,
            'API_SECRET': api_secret,
        }
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )
    else:
        CLOUDINARY_STORAGE = {'CLOUDINARY_URL': CLOUDINARY_URL}
else:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    cloudinary.config(
        cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key=os.environ.get('CLOUDINARY_API_KEY'),
        api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
        secure=True
    )

# Suporte de armazenamento para Django
# Usa Cloudinary somente se houver credenciais configuradas; caso contrário,
# guarda as imagens localmente na pasta media/ do próprio servidor.
_MEDIA_STORAGE_BACKEND = (
    'cloudinary_storage.storage.MediaCloudinaryStorage'
    if USE_CLOUDINARY
    else 'django.core.files.storage.FileSystemStorage'
)

STORAGES = {
    "default": {
        "BACKEND": _MEDIA_STORAGE_BACKEND,
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

DEFAULT_FILE_STORAGE = _MEDIA_STORAGE_BACKEND

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'