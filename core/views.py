from django.shortcuts import render
from .models import Perfume, Campanha
from django.db.utils import ProgrammingError, OperationalError

def home(request):
    # O .order_by('-id') garante que os últimos perfumes cadastrados venham primeiro
    lancamentos = Perfume.objects.all().order_by('-id')[:10]
    
    # Busca a campanha. Se a tabela ainda não existir no banco, ignora para não dar erro 500
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
    # Ordena do mais recente para o mais antigo na página de coleção também
    perfumes = Perfume.objects.all().order_by('-id')
    
    genero = request.GET.get('genero')
    marca = request.GET.get('marca')

    if genero:
        perfumes = perfumes.filter(genero=genero)
    if marca:
        perfumes = perfumes.filter(marca=marca)

    context = {
        'perfumes': perfumes,
        'genero_selecionado': genero,
        'marca_selecionada': marca,
    }
    return render(request, 'core/colecao.html', context)