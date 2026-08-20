from django.contrib import admin
from django.db import connection
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Perfume, Campanha, CampanhaPerfume

def limpar_tabela_antiga():
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS core_campanha_perfumes CASCADE;")
    except Exception:
        pass

limpar_tabela_antiga()


class CampanhaPerfumeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CampanhaPerfume
    extra = 1
    autocomplete_fields = ['perfume']


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco_custo', 'preco', 'exibir_lucro', 'exibir_porcentagem', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('valor_lucro', 'porcentagem_lucro')

    def exibir_lucro(self, obj):
        return f"R$ {obj.valor_lucro:.2f}"
    exibir_lucro.short_description = "Lucro (R$)"

    def exibir_porcentagem(self, obj):
        return f"{obj.porcentagem_lucro:.1f}%"
    exibir_porcentagem.short_description = "Margem (%)"

    def delete_model(self, request, obj):
        limpar_tabela_antiga()
        super().delete_model(request, obj)


@admin.register(Campanha)
class CampanhaAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    inlines = [CampanhaPerfumeInline]