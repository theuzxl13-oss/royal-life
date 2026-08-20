from django.shortcuts import render
from django.db.utils import ProgrammingError, OperationalError
from .models import Perfume, Campanha, Marca

def home(request):
    # Traz os perfumes cadastrados mais recentes primeiro (máximo 10)
    lancamentos = Perfume.objects.all().order_by('-id')[:10]

    # Busca a campanha ativa
    try:
        campanha_ativa = Campanha.objects.filter(ativa=True).first()
    except (ProgrammingError, OperationalError):
        campanha_ativa = None

    context = {
        'lancamentos': lancamentos,
        'campanha_ativa': campanha_ativa,
    }
    return render(request, 'core/home.html', context)


def colecao(request):
    # Ordena do mais recente para o mais antigo na coleção
    perfumes = Perfume.objects.all().order_by('-id')
    
    genero = request.GET.get('genero')
    marca_slug = request.GET.get('marca')

    if genero:
        perfumes = perfumes.filter(genero=genero)
    if marca_slug:
        perfumes = perfumes.filter(marca__slug=marca_slug)

    try:
        marcas = Marca.objects.all().order_by('nome')
    except (ProgrammingError, OperationalError):
        marcas = []

    context = {
        'perfumes': perfumes,
        'marcas': marcas,
        'genero_selecionado': genero,
        'marca_selecionada': marca_slug,
    }
    return render(request, 'core/colecao.html', context)


# Limiar mínimo de parecença para considerar uma foto como "compatível".
# 1.0 = idêntica, valores acima de ~0.75 costumam indicar o mesmo produto.
LIMIAR_SIMILARIDADE = 0.75


def busca_foto(request):
    resultados = []
    erro = None

    if request.method == 'POST' and request.FILES.get('foto'):
        try:
            from PIL import Image
            from .clip_utils import compute_embedding, cosine_similarity

            with Image.open(request.FILES['foto']) as img:
                consulta = compute_embedding(img.convert('RGB'))

            candidatos = Perfume.objects.exclude(imagem_embedding__isnull=True).select_related('marca')

            pontuados = []
            for perfume in candidatos:
                similaridade = cosine_similarity(consulta, perfume.imagem_embedding)
                if similaridade >= LIMIAR_SIMILARIDADE:
                    pontuados.append((similaridade, perfume))

            pontuados.sort(key=lambda item: item[0], reverse=True)

            resultados = [
                {'perfume': perfume, 'similaridade': round(similaridade * 100)}
                for similaridade, perfume in pontuados[:5]
            ]

            if not resultados:
                erro = "Não encontramos nenhum perfume parecido no nosso catálogo. Tente outra foto ou fale com a gente pelo WhatsApp."
        except Exception:
            erro = "Não foi possível processar essa imagem. Tente novamente com outra foto (JPG ou PNG)."

    return render(request, 'core/busca_foto.html', {'resultados': resultados, 'erro': erro})