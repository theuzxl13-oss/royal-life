import os
from pathlib import Path
import dj_database_url

# Diretorio base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# CHAVE DE SEGURANÇA
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sua-chave-secreta-aqui')

# DEBUG: Desativa em produção se houver variável RENDER
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = ['*']

# APPS INSTALADOS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # App do projeto
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir arquivos estaticos no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Nome da pasta principal onde fica o wsgi.py e urls.py principal
# Se o seu projeto tiver outro nome de pasta principal (ex: setup), altere abaixo:
ROOT_URLCONF = 'royallife.urls'

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

WSGI_APPLICATION = 'royallife.wsgi.application'

# BANCO DE DADOS (Usa Neon no Render via DATABASE_URL e SQLite no PC)
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

# ARQUIVOS ESTÁTICOS (CSS, JS, Imagens do site)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ARQUIVOS DE MÍDIA (Fotos dos perfumes enviadas no Admin)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CONFIGURAÇÃO DE CHAVE PRIMÁRIA
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'