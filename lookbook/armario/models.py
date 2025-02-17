from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=True, null=True)  # Verano, Invierno, etc.

    def __str__(self):
        return self.nombre

from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Outfit(models.Model):
    foto = models.ImageField(upload_to='outfits/', null=True)  

    etiqueta = models.ForeignKey('Etiqueta', on_delete=models.CASCADE, null=True)
    creado_en = models.DateTimeField(auto_now_add=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfits", null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la imagen original

        if self.foto:
            img_path = self.foto.path
            max_size = (800, 800)  # Ajusta el tamaño máximo según tus necesidades

            with Image.open(img_path) as img:
                img.thumbnail(max_size)  # Redimensiona manteniendo la proporción
                img.save(img_path, optimize=True, quality=80)  # Optimiza la imagen con buena calidad

    def __str__(self):
        return f"Outfit {self.id} - {self.etiqueta.nombre}"

# class Outfit(models.Model):
#     foto = models.ImageField(upload_to='outfits/', null=True)  # Asegúrate de que esta línea esté presente
#     etiqueta = models.ForeignKey('Etiqueta', on_delete=models.CASCADE, null=True)
#     creado_en = models.DateTimeField(auto_now_add=True, null=True)
#     creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="outfits", null=True)

#     def __str__(self):
#         return f"Outfit {self.id} - {self.etiqueta.nombre}"


class Prenda(models.Model):
    TIPO_PRENDA = [
        ('parte_arriba', 'Parte de arriba'),
        ('pantalones', 'Pantalones'),
        ('zapatos', 'Zapatos'),
        ('accesorios', 'Accesorios'),
    ]
    
    outfit = models.ForeignKey(Outfit, related_name='prendas', on_delete=models.CASCADE, null=True)  # Relación con el outfit
    nombre = models.CharField(max_length=100, null=True)  # Nombre de la prenda
    enlace_compra = models.URLField(null=True)  # Link de compra
    tipo = models.CharField(max_length=15, choices=TIPO_PRENDA, null=True)  # Tipo de prenda (parte de arriba, pantalones, zapatos)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    numero_telefono = models.CharField(max_length=15, blank=True, null=True, verbose_name="Número de Teléfono")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografía")
    marca_favorita = models.CharField(max_length=100, blank=True, null=True, verbose_name="Marca Favorita")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(usuario=instance)

@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()


class Valoracion(models.Model):
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='valoraciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.PositiveIntegerField(default=0)  # Valoración del 1 al 5

    class Meta:
        unique_together = ('outfit', 'usuario')  # Cada usuario solo puede valorar un outfit una vez
