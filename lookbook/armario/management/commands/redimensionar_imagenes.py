from django.core.management.base import BaseCommand
from PIL import Image
from django.conf import settings
from armario.models import Outfit  # Ajusta la importación a tu modelo correcto
import os

class Command(BaseCommand):
    help = 'Redimensiona las imágenes de los outfits ya subidos.'

    def handle(self, *args, **kwargs):
        # Definir el tamaño máximo para las imágenes
        max_size = (800, 800)

        # Obtener todas las imágenes de outfits
        outfits = Outfit.objects.all()

        for outfit in outfits:
            if outfit.foto:
                img_path = outfit.foto.path  # Ruta de la imagen
                try:
                    with Image.open(img_path) as img:
                        img.thumbnail(max_size)  # Redimensionar la imagen
                        img.save(img_path, optimize=True, quality=80)  # Guardar la imagen con calidad optimizada
                        self.stdout.write(self.style.SUCCESS(f'Imagen redimensionada: {outfit.foto.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error al redimensionar la imagen {outfit.foto.name}: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Outfit sin imagen: {outfit.id}'))

