from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User
from django.http import HttpResponse
from core import views

def reset_admin(request):
    user, created = User.objects.get_or_create(username='admin')
    user.set_password('Admin123456') # Definindo a senha temporária
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return HttpResponse("✅ Usuário 'admin' atualizado com sucesso! A nova senha é: Admin123456")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reset-admin/', reset_admin), # Rota de reset
    path('', views.home, name='home'),
    path('colecao/', views.colecao, name='colecao'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)