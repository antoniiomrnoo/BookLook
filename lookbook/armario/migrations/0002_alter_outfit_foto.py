# Generated by Django 5.1.1 on 2024-10-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='foto',
            field=models.ImageField(upload_to='media/outfits'),
        ),
    ]