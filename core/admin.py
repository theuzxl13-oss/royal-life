from django.contrib import admin
from .models import Perfume, PerfumeMasculino, PerfumeFeminino, PerfumeUnissex

class BasePerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco', 'estoque', 'criado_em')
    list_filter = ('marca',)
    search_fields = ('nome', 'descricao')
    fields = ('nome', 'marca', 'preco', 'estoque', 'descricao', 'imagem', 'notas_saida', 'notas_coracao', 'notas_fundo')

@admin.register(PerfumeMasculino)
class PerfumeMasculinoAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'masculino'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='masculino')


@admin.register(PerfumeFeminino)
class PerfumeFemininoAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'feminino'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='feminino')


@admin.register(PerfumeUnissex)
class PerfumeUnissexAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'unissex'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='unissex')


@admin.register(Perfume)
class PerfumeGeralAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'marca', 'preco', 'estoque')
    list_filter = ('genero', 'marca')
    search_fields = ('nome',)