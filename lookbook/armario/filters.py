# filters.py
from django_filters import rest_framework as filters
from .models import Prenda, Etiqueta
from django.db import models

class EtiquetaFilter(filters.FilterSet):
    class Meta:
        model = Etiqueta
        fields = '__all__'  # Permite filtrar por cualquier campo del modelo

        # Ignora el campo ImageField estableciendo una anulaciÃ³n
        filter_overrides = {
            models.ImageField: {
                'filter_class': filters.CharFilter  # Usa un filtro de texto para ignorar las imÃ¡genes
            }
        }


class PrendaFilter(filters.FilterSet):
    class Meta:
        model = Prenda
        fields = '__all__'  # Permite filtrar por cualquier campo del modelo

        # Si algÃºn campo es de tipo ImageField, se ignora o se le asigna un filtro adecuado
        filter_overrides = {
            models.ImageField: {
                'filter_class': filters.CharFilter  # Usa un filtro de texto para ignorar las imÃ¡genes
            }
        }