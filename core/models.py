from django.db import models

class Produto(models.Model):
    # Opções de gênero
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('unissex', 'Unissex'),
    ]

    # Opções de marca
    MARCA_CHOICES = [
        ('lattafa', 'Lattafa'),
        ('armaf', 'Armaf'),
        ('afnan', 'Afnan'),
        ('maison-alhambra', 'Maison Alhambra'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Produto")
    genero = models.CharField(max_length=15, choices=GENERO_CHOICES, verbose_name="Gênero")
    marca = models.CharField(max_length=30, choices=MARCA_CHOICES, verbose_name="Marca")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True, verbose_name="Imagem")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.nome} ({self.get_genero_display()} - {self.get_marca_display()})"