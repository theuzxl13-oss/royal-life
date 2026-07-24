from django.shortcuts import render
from .models import Perfume

def home(request):
    return render(request, 'core/home.html')

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