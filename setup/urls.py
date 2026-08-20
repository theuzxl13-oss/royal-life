from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.models import User
from django.http import HttpResponse
from core import views

def reset_admin(request):
    user, created = User.objects.get_or_create(username='admin')
    user.set_password('Admin123456')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return HttpResponse("✅ Usuário 'admin' atualizado com sucesso! A nova senha é: Admin123456")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reset-admin/', reset_admin),
    path('', views.home, name='home'),
    path('colecao/', views.colecao, name='colecao'),
    
    # Permite exibir imagens da pasta media no Render
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)