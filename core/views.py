from django.shortcuts import render
from .models import Perfume, Campanha
from django.db.utils import ProgrammingError, OperationalError

def home(request):
    lancamentos = Perfume.objects.all()[:4]
    
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
    perfumes = Perfume.objects.all()
    
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