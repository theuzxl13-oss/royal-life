from django.db import migrations
from django.utils.text import slugify

MARCAS = [
    'Niche Avenue', 'Al Fares', 'Abdul Samad Al Qurashi', 'Afnan',
    'Al Haramain', 'Al Wataniah', 'Ard Al Zaafaran', 'Armaf',
    'Lattafa', 'Maison Alhambra', 'Fragrance World', 'Asdaaf',
    'Aurora Scents', 'French Avenue', 'Le Chameau', 'Manasik',
    'Rasasi', 'Rave', 'Rayhaan', 'Riifs', 'Zimaya', 'Orientica',
    'Nusuk', 'Emper', 'Bharara', 'Mirada Shield', 'Sahari',
    'Ohana Kameala', 'Bekim', 'La Chameau', 'Gissat', 'Milestone',
    'Prelitzy', 'Body Care', 'MPF', 'Medicube - K Beauty',
    'Celimax - K Beauty', 'Numbuzin - K Beauty', 'Sungboon Editor - K Beauty',
    'Arabyat Prestige', 'Ameerati', 'Dream Collection', 'Mamlakat Al Oud',
]


def popular_marcas(apps, schema_editor):
    Marca = apps.get_model('core', 'Marca')
    for nome in MARCAS:
        Marca.objects.get_or_create(nome=nome, defaults={'slug': slugify(nome)})


def remover_marcas(apps, schema_editor):
    Marca = apps.get_model('core', 'Marca')
    Marca.objects.filter(nome__in=MARCAS).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(popular_marcas, remover_marcas),
    ]
