from django.contrib import admin
from django.db import connection
from django.utils.text import slugify
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Marca, Perfume, Campanha, CampanhaPerfume

def migrar_estrutura_e_popular_marcas():
    """Garante a criação da tabela de marcas, a coluna marca_id no banco e insere todas as marcas extraídas."""
    try:
        with connection.cursor() as cursor:
            # 1. Cria a tabela de marcas se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_marca (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) UNIQUE NOT NULL,
                    slug VARCHAR(100) UNIQUE NOT NULL
                );
            """)
            
            # 2. Lista completa de marcas extraídas das imagens
            marcas_lista = [
                'Niche Avenue', 'Al Fares', 'Abdul Samad Al Qurashi', 'Afnan',
                'Al Haramain', 'Al Wataniah', 'Ard Al Zaafaran', 'Armaf',
                'Lattafa', 'Maison Alhambra', 'Fragrance World', 'Asdaaf',
                'Aurora Scents', 'French Avenue', 'Le Chameau', 'Manasik',
                'Rasasi', 'Rave', 'Rayhaan', 'Riifs', 'Zimaya', 'Orientica',
                'Nusuk', 'Emper', 'Bharara', 'Mirada Shield', 'Sahari',
                'Ohana Kameala', 'Bekim', 'La Chameau', 'Gissat', 'Milestone',
                'Prelitzy', 'Body Care', 'MPF', 'Medicube - K Beauty',
                'Celimax - K Beauty', 'Numbuzin - K Beauty', 'Sungboon Editor - K Beauty',
                'Arabyat Prestige', 'Ameerati', 'Dream Collection', 'Mamlakat Al Oud'
            ]

            # Inserção segura no banco sem duplicar
            for nome_marca in marcas_lista:
                slug_marca = slugify(nome_marca)
                cursor.execute("""
                    INSERT INTO core_marca (nome, slug)
                    VALUES (%s, %s)
                    ON CONFLICT (nome) DO NOTHING;
                """, [nome_marca, slug_marca])

            # 3. Adiciona a coluna marca_id se ela não existir em core_perfume
            cursor.execute("""
                ALTER TABLE core_perfume 
                ADD COLUMN IF NOT EXISTS marca_id INTEGER REFERENCES core_marca(id);
            """)

            # 4. Aponta qualquer registro antigo sem marca para o ID 1
            cursor.execute("UPDATE core_perfume SET marca_id = 1 WHERE marca_id IS NULL;")
            
            # 5. Remove a coluna texto antiga 'marca' caso exista
            cursor.execute("ALTER TABLE core_perfume DROP COLUMN IF EXISTS marca;")
    except Exception:
        pass

migrar_estrutura_e_popular_marcas()


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