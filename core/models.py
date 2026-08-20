from django.db import models

class Marca(models.Model):
    nome = models.CharField("Nome da Marca", max_length=100, unique=True)
    slug = models.SlugField("Identificador na URL", max_length=100, unique=True, blank=True, help_text="Gerado automaticamente se deixar em branco")

    class Meta:
        ordering = ['nome']
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Perfume(models.Model):
    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('unissex', 'Unissex'),
    ]

    nome = models.CharField("Nome do Perfume", max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='perfumes', verbose_name="Marca")
    genero = models.CharField("Gênero", max_length=20, choices=GENERO_CHOICES, default='unissex')
    
    # Preços e Financeiro
    preco_custo = models.DecimalField("Preço de Custo (R$)", max_digits=10, decimal_places=2, default=0.00, help_text="Quanto você pagou no perfume")
    preco = models.DecimalField("Preço de Venda (R$)", max_digits=10, decimal_places=2)

    descricao = models.TextField("Descrição", blank=True, null=True)
    imagem = models.ImageField("Imagem", upload_to='perfumes/', blank=True, null=True)
    estoque = models.IntegerField("Estoque", default=0)
    
    # Notas Olfativas
    notas_saida = models.CharField("Notas de Saída", max_length=200, blank=True, null=True)
    notas_coracao = models.CharField("Notas de Coração", max_length=200, blank=True, null=True)
    notas_fundo = models.CharField("Notas de Fundo", max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Perfume"
        verbose_name_plural = "Perfumes"

    @property
    def valor_lucro(self):
        if self.preco and self.preco_custo is not None:
            return self.preco - self.preco_custo
        return 0.00

    @property
    def porcentagem_lucro(self):
        if self.preco_custo and self.preco_custo > 0:
            return ((self.preco - self.preco_custo) / self.preco_custo) * 100
        return 100.00 if (self.preco and self.preco > 0) else 0.00

    def __str__(self):
        return self.nome


class Campanha(models.Model):
    titulo = models.CharField("Título", max_length=100, help_text="Ex: Promoção de Dia dos Pais")
    subtitulo = models.CharField("Subtítulo", max_length=200, blank=True, null=True, help_text="Ex: Até 30% OFF em fragrâncias marcantes")
    ativa = models.BooleanField("Ativa", default=True, help_text="Marque para exibir no site")
    perfumes = models.ManyToManyField(Perfume, through='CampanhaPerfume', related_name='campanhas', blank=True)

    class Meta:
        verbose_name = "Campanha"
        verbose_name_plural = "Campanhas"

    def __str__(self):
        return self.titulo


class CampanhaPerfume(models.Model):
    campanha = models.ForeignKey(Campanha, on_delete=models.CASCADE, related_name='campanhaperfume_set')
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='campanha_perfumes')
    ordem = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        try:
            nome_perfume = self.perfume.nome if self.perfume_id else "Sem Perfume"
        except Exception:
            nome_perfume = "Sem Perfume"

        try:
            titulo_campanha = self.campanha.titulo if self.campanha_id else "Sem Campanha"
        except Exception:
            titulo_campanha = "Sem Campanha"

        return f"{nome_perfume} - {titulo_campanha}"