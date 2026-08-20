from django.contrib import admin
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Marca, Perfume, Campanha, CampanhaPerfume

admin.site.site_header = "Royal Life"
admin.site.site_title = "Royal Life Admin"
admin.site.index_title = "Painel de Administração"


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    prepopulated_fields = {'slug': ('nome',)}


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