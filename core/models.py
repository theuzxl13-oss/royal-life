from django.db import models

class Perfume(models.Model):
    MARCAS_CHOICES = [
        ('lattafa', 'Lattafa'),
        ('armaf', 'Armaf'),
        ('afnan', 'Afnan'),
        ('maison-alhambra', 'Maison Alhambra'),
    ]

    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('unissex', 'Unissex'),
    ]

    nome = models.CharField(max_length=100)
    marca = models.CharField(max_length=50, choices=MARCAS_CHOICES)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, default='unissex')
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='perfumes/', blank=True, null=True)
    estoque = models.IntegerField(default=0)
    
    # Notas Olfativas
    notas_saida = models.CharField(max_length=200, blank=True, null=True)
    notas_coracao = models.CharField(max_length=200, blank=True, null=True)
    notas_fundo = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome


class Campanha(models.Model):
    titulo = models.CharField(max_length=100, help_text="Ex: Promoção de Dia dos Pais")
    subtitulo = models.CharField(max_length=200, blank=True, null=True, help_text="Ex: Até 30% OFF em fragrâncias marcantes")
    ativa = models.BooleanField(default=True, help_text="Marque para exibir no site")
    perfumes = models.ManyToManyField(Perfume, related_name='campanhas', blank=True)

    def __str__(self):
        return self.titulo