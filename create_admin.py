import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

USERNAME = 'admin'
EMAIL = 'admin@royallife.com'
PASSWORD = 'admin'

user, created = User.objects.get_or_create(username=USERNAME, defaults={'email': EMAIL})
user.set_password(PASSWORD)
user.is_staff = True
user.is_superuser = True
user.save()

if created:
    print("Superusuario criado com sucesso!")
else:
    print("Senha do superusuario atualizada com sucesso!")