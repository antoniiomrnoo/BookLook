from django.db import models

# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)  # Verano, Invierno, etc.

    def __str__(self):
        return self.nombre

class Outfit(models.Model):
    foto = models.ImageField(upload_to='outfits/')  # Foto del outfit
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.CASCADE)  # Relación con la etiqueta (verano/invierno)
    creado_en = models.DateTimeField(auto_now_add=True)  # Fecha de creación

    def __str__(self):
        return f"Outfit {self.id} - {self.etiqueta.nombre}"

class Prenda(models.Model):
    TIPO_PRENDA = [
        ('parte_arriba', 'Parte de arriba'),
        ('pantalones', 'Pantalones'),
        ('zapatos', 'Zapatos'),
    ]
    
    outfit = models.ForeignKey(Outfit, related_name='prendas', on_delete=models.CASCADE)  # Relación con el outfit
    nombre = models.CharField(max_length=100)  # Nombre de la prenda
    enlace_compra = models.URLField()  # Link de compra
    tipo = models.CharField(max_length=15, choices=TIPO_PRENDA)  # Tipo de prenda (parte de arriba, pantalones, zapatos)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"