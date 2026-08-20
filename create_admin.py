import os
import django

# Configura as variaveis do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Dados do seu usuario administrador
USERNAME = 'admin'
EMAIL = 'admin@royallife.com'
PASSWORD = 'admin'  # Você pode trocar por outra senha se quiser

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(username=USERNAME, email=EMAIL, password=PASSWORD)
    print(f"Superusuario '{USERNAME}' criado com sucesso!")
else:
    print(f"Superusuario '{USERNAME}' ja existe.")