# Generated by Django 5.1.1 on 2024-10-23 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armario', '0003_remove_outfit_foto_remove_prenda_outfit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfit',
            name='creador',
        ),
        migrations.RemoveField(
            model_name='outfit',
            name='imagen',
        ),
        migrations.RemoveField(
            model_name='outfit',
            name='pantalones',
        ),
        migrations.RemoveField(
            model_name='outfit',
            name='parte_superior',
        ),
        migrations.RemoveField(
            model_name='outfit',
            name='zapatos',
        ),
        migrations.AddField(
            model_name='outfit',
            name='foto',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
        migrations.AddField(
            model_name='prenda',
            name='outfit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prendas', to='armario.outfit'),
        ),
        migrations.AlterField(
            model_name='etiqueta',
            name='nombre',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='creado_en',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='etiqueta',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='armario.etiqueta'),
        ),
        migrations.AlterField(
            model_name='prenda',
            name='enlace_compra',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='prenda',
            name='nombre',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='prenda',
            name='tipo',
            field=models.CharField(choices=[('parte_arriba', 'Parte de arriba'), ('pantalones', 'Pantalones'), ('zapatos', 'Zapatos')], max_length=15, null=True),
        ),
    ]