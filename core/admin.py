from django.contrib import admin
from django.db import connection
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from .models import Marca, Perfume, Campanha, CampanhaPerfume

def migrar_estrutura_marcas():
    """Cria a tabela de marcas e ajusta a coluna marca na tabela core_perfume se necessário."""
    try:
        with connection.cursor() as cursor:
            # Cria a tabela core_marca se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS core_marca (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) UNIQUE NOT NULL,
                    slug VARCHAR(100) UNIQUE NOT NULL
                );
            """)
            
            # Garante marcas padrão
            marcas_padrao = [
                ('Lattafa', 'lattafa'),
                ('Armaf', 'armaf'),
                ('Afnan', 'afnan'),
                ('Maison Alhambra', 'maison-alhambra')
            ]
            for nome, slug in marcas_padrao:
                cursor.execute("""
                    INSERT INTO core_marca (nome, slug)
                    VALUES (%s, %s)
                    ON CONFLICT (nome) DO NOTHING;
                """, [nome, slug])

            # Verifica o tipo da coluna marca em core_perfume
            cursor.execute("""
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = 'core_perfume' AND column_name = 'marca_id';
            """)
            has_marca_id = cursor.fetchone()

            if not has_marca_id:
                # Transforma a coluna texto em marca_id relacionando com core_marca
                cursor.execute("ALTER TABLE core_perfume RENAME COLUMN marca TO marca_old;")
                cursor.execute("ALTER TABLE core_perfume ADD COLUMN marca_id INTEGER REFERENCES core_marca(id);")
                cursor.execute("""
                    UPDATE core_perfume p
                    SET marca_id = m.id
                    FROM core_marca m
                    WHERE LOWER(p.marca_old) = LOWER(m.slug) OR LOWER(p.marca_old) = LOWER(m.nome);
                """)
                # Marca ID 1 caso algum fique sem
                cursor.execute("UPDATE core_perfume SET marca_id = 1 WHERE marca_id IS NULL;")
                cursor.execute("ALTER TABLE core_perfume ALTER COLUMN marca_id SET NOT NULL;")
                cursor.execute("ALTER TABLE core_perfume DROP COLUMN IF EXISTS marca_old;")
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