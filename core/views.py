from django.shortcuts import render
from .models import Perfume

def home(request):
    perfumes = Perfume.objects.all()
    return render(request, 'core/home.html', {'perfumes': perfumes})