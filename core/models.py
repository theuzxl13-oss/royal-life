from django.db import models

class Perfume(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('unissex', 'Unissex'),
    ]

    MARCA_CHOICES = [
        ('lattafa', 'Lattafa'),
        ('armaf', 'Armaf'),
        ('afnan', 'Afnan'),
        ('maison-alhambra', 'Maison Alhambra'),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do Perfume")
    genero = models.CharField(max_length=15, choices=GENERO_CHOICES, verbose_name="Gênero")
    marca = models.CharField(max_length=30, choices=MARCA_CHOICES, verbose_name="Marca")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço (R$)")
    estoque = models.IntegerField(default=0, blank=True, null=True, verbose_name="Estoque")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    imagem = models.ImageField(upload_to='perfumes/', blank=True, null=True, verbose_name="Imagem")

    notas_saida = models.CharField(max_length=255, blank=True, null=True, verbose_name="Notas de Saída")
    notas_coracao = models.CharField(max_length=255, blank=True, null=True, verbose_name="Notas de Coração")
    notas_fundo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Notas de Fundo")

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Todos os Perfumes"
        verbose_name_plural = "Todos os Perfumes"

    def __str__(self):
        return f"{self.nome} - {self.get_marca_display()}"


class PerfumeMasculino(Perfume):
    class Meta:
        proxy = True
        verbose_name = "Perfume Masculino"
        verbose_name_plural = "1. PERFUMES MASCULINOS"


class PerfumeFeminino(Perfume):
    class Meta:
        proxy = True
        verbose_name = "Perfume Feminino"
        verbose_name_plural = "2. PERFUMES FEMININOS"


class PerfumeUnissex(Perfume):
    class Meta:
        proxy = True
        verbose_name = "Perfume Unissex"
        verbose_name_plural = "3. PERFUMES UNISSEX"