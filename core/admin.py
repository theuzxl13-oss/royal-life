from django.contrib import admin
from .models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    # Divisão do formulário de cadastro em blocos/etapas bem organizados
    fieldsets = (
        ('1. Informações do Perfume', {
            'fields': ('nome', 'descricao'),
            'description': 'Preencha o nome comercial e os detalhes/notas olfativas do perfume.'
        }),
        ('2. Categorização (Gênero e Marca)', {
            'fields': ('genero', 'marca'),
            'description': 'Defina se é Masculino/Feminino/Unissex e a marca correspondente.'
        }),
        ('3. Valor e Imagem', {
            'fields': ('preco', 'imagem'),
            'description': 'Informe o preço de venda e escolha a foto principal do perfume.'
        }),
    )

    # Exibição na tabela de listagem dos produtos cadastrados
    list_display = ('nome', 'marca_formatada', 'genero_formatado', 'preco_formatado', 'criado_em')
    list_filter = ('genero', 'marca')
    search_fields = ('nome', 'descricao')
    list_per_page = 25

    # Métodos para formatar a exibição dos campos na tabela
    @admin.display(description='Gênero')
    def genero_formatado(self, obj):
        return obj.get_genero_display()

    @admin.display(description='Marca')
    def marca_formatada(self, obj):
        return obj.get_marca_display()

    @admin.display(description='Preço')
    def preco_formatado(self, obj):
        return f"R$ {obj.preco:.2f}".replace('.', ',')