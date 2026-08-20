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

    # Puxa todas as marcas cadastradas para o menu lateral
    try:
        marcas = Marca.objects.all().order_by('nome')
    except (ProgrammingError, OperationalError):
        marcas = []

    context = {
        'lancamentos': lancamentos,
        'campanha_ativa': campanha_ativa,
        'marcas': marcas,
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