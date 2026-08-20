from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin
from .models import Perfume, Campanha, CampanhaPerfume

# Classe para permitir arrastar e soltar os perfumes na campanha
class CampanhaPerfumeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CampanhaPerfume
    extra = 1
    autocomplete_fields = ['perfume'] # Facilita a busca de perfumes se tiver muitos

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'genero', 'preco', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    inlines = [CampanhaPerfumeInline] # Subsitui o filter_horizontal pela tabela arrastável