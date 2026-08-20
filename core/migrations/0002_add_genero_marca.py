from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),  # Depende da primeira migração
    ]

    operations = [
        migrations.AddField(
            model_name='perfume',
            name='genero',
            field=models.CharField(
                choices=[('masculino', 'Masculino'), ('feminino', 'Feminino'), ('unissex', 'Unissex')],
                default='unissex',
                max_length=15,
                verbose_name='Gênero'
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='perfume',
            name='marca',
            field=models.CharField(
                choices=[('lattafa', 'Lattafa'), ('armaf', 'Armaf'), ('afnan', 'Afnan'), ('maison-alhambra', 'Maison Alhambra')],
                default='lattafa',
                max_length=30,
                verbose_name='Marca'
            ),
            preserve_default=False,
        ),
    ]