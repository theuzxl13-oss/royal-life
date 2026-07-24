from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, colecao

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('colecao/', colecao, name='colecao'),
]

# Libera o acesso às imagens cadastradas no admin
if settings.DEBUG or True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)