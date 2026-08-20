from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Campos que vão aparecer na tabela de listagem do admin
    list_display = ('nome', 'genero', 'marca', 'preco', 'criado_em')
    
    # Filtros que aparecem na barra lateral direita no admin
    list_filter = ('genero', 'marca')
    
    # Campo de busca no topo da página do admin
    search_fields = ('nome', 'descricao')