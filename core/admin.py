from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Perfume, Campanha, CampanhaPerfume

# Classe para permitir arrastar e soltar os perfumes na campanha
class CampanhaPerfumeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CampanhaPerfume
    extra = 1
    autocomplete_fields = ['perfume']

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'genero', 'preco', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')

# Adicionado SortableAdminBase aqui na herança da CampanhaAdmin
@admin.register(Campanha)
class CampanhaAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    inlines = [CampanhaPerfumeInline]