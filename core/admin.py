from django.contrib import admin
from .models import Perfume, PerfumeMasculino, PerfumeFeminino, PerfumeUnissex

# Classe base para reaproveitar a configuração dos campos
class BasePerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'preco', 'criado_em')
    list_filter = ('marca',)
    search_fields = ('nome', 'descricao')
    fields = ('nome', 'marca', 'preco', 'descricao', 'imagem')

# 1. Painel Masculino (Já preenche o gênero como masculino automaticamente)
@admin.register(PerfumeMasculino)
class PerfumeMasculinoAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'masculino'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='masculino')


# 2. Painel Feminino (Já preenche o gênero como feminino automaticamente)
@admin.register(PerfumeFeminino)
class PerfumeFemininoAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'feminino'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='feminino')


# 3. Painel Unissex (Já preenche o gênero como unissex automaticamente)
@admin.register(PerfumeUnissex)
class PerfumeUnissexAdmin(BasePerfumeAdmin):
    def save_model(self, request, obj, form, change):
        obj.genero = 'unissex'
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(genero='unissex')


# Registra também o modelo geral de todos os perfumes
@admin.register(Perfume)
class PerfumeGeralAdmin(admin.ModelAdmin):
    list_display = ('nome', 'genero', 'marca', 'preco')
    list_filter = ('genero', 'marca')
    search_fields = ('nome',)