from django.shortcuts import render
from .models import Perfume

def home(request):
    # Pega os 4 últimos perfumes cadastrados para exibir em Destaques/Lançamentos
    lancamentos = Perfume.objects.all().order_by('-criado_em')[:4]
    return render(request, 'core/home.html', {'lancamentos': lancamentos})

def colecao(request):
    genero = request.GET.get('genero')
    marca = request.GET.get('marca')
    
    perfumes = Perfume.objects.all()
    
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