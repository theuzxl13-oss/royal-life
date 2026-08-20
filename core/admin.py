from django.contrib import admin
from django.db import connection
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Perfume, Campanha, CampanhaPerfume

# Remove a tabela antiga travada do banco PostgreSQL automaticamente
def limpar_tabela_antiga():
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS core_campanha_perfumes CASCADE;")
    except Exception:
        pass

# Executa a limpeza assim que o Admin é carregado
limpar_tabela_antiga()


class CampanhaPerfumeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CampanhaPerfume
    extra = 1
    autocomplete_fields = ['perfume']


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'genero', 'preco', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')

    def delete_model(self, request, obj):
        limpar_tabela_antiga()
        super().delete_model(request, obj)


@admin.register(Campanha)
class CampanhaAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    inlines = [CampanhaPerfumeInline]