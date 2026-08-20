from django.contrib import admin
from django.db import connection
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Perfume, Campanha, CampanhaPerfume

def garantir_coluna_custo():
    """Garante que a coluna preco_custo exista no banco de dados sem dar erro."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE core_perfume ADD COLUMN IF NOT EXISTS preco_custo numeric(10,2) DEFAULT 0.00;")
    except Exception:
        pass

garantir_coluna_custo()


class CampanhaPerfumeInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CampanhaPerfume
    extra = 1
    autocomplete_fields = ['perfume']


@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco_custo', 'preco', 'exibir_lucro', 'exibir_porcentagem', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')
    readonly_fields = ('exibir_lucro', 'exibir_porcentagem')

    def exibir_lucro(self, obj):
        return f"R$ {obj.valor_lucro:.2f}"
    exibir_lucro.short_description = "Valor do Lucro (R$)"

    def exibir_porcentagem(self, obj):
        return f"{obj.porcentagem_lucro:.1f}%"
    exibir_porcentagem.short_description = "Margem de Lucro (%)"


@admin.register(Campanha)
class CampanhaAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    inlines = [CampanhaPerfumeInline]