from django.contrib import admin
from .models import Perfume, Campanha

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'marca', 'genero', 'preco', 'estoque')
    list_filter = ('marca', 'genero')
    search_fields = ('nome', 'descricao')

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa')
    list_editable = ('ativa',)
    filter_horizontal = ('perfumes',)