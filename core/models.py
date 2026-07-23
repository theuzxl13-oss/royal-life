from django.db import models

class Perfume(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Perfume")
    imagem = models.ImageField(upload_to='perfumes/', null=True, blank=True, verbose_name="Imagem do Perfume")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preco")
    descricao = models.TextField(verbose_name="Descricao")
    
    # Piramide Olfativa
    notas_saida = models.CharField(max_length=200, verbose_name="Notas de Saida (Topo)")
    notas_coracao = models.CharField(max_length=200, verbose_name="Notas de Coracao (Corpo)")
    notas_fundo = models.CharField(max_length=200, verbose_name="Notas de Fundo (Base)")
    
    estoque = models.IntegerField(default=10, verbose_name="Quantidade em Estoque")
    
    def __str__(self):
        return self.nome