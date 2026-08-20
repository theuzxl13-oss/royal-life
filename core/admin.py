from django.contrib import admin
from django.db import connection
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Marca, Perfume, Campanha, CampanhaPerfume

def migrar_estrutura_marcas():
    """Garante a criação da tabela de marcas e a coluna marca_id no banco."""
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
            
            # 2. Insere as marcas padrão
            marcas = [
                ('Lattafa', 'lattafa'),
                ('Armaf', 'armaf'),
                ('Afnan', 'afnan'),
                ('Maison Alhambra', 'maison-alhambra')
            ]
            for nome, slug in marcas:
                cursor.execute("""
                    INSERT INTO core_marca (nome, slug)
                    VALUES (%s, %s)
                    ON CONFLICT (nome) DO NOTHING;
                """, [nome, slug])

            # 3. Adiciona a coluna marca_id se ela não existir em core_perfume
            cursor.execute("""
                ALTER TABLE core_perfume 
                ADD COLUMN IF NOT EXISTS marca_id INTEGER REFERENCES core_marca(id);
            """)

            # 4. Aponta qualquer registro antigo para a marca padrão (ID 1) caso esteja nulo
            cursor.execute("UPDATE core_perfume SET marca_id = 1 WHERE marca_id IS NULL;")
            
            # 5. Se ainda existir a coluna texto antiga 'marca', remove para evitar conflito
            cursor.execute("ALTER TABLE core_perfume DROP COLUMN IF EXISTS marca;")
    except Exception:
        pass

migrar_estrutura_marcas()


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