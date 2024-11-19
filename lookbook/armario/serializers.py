# serializers.py
from rest_framework import serializers
from .models import Outfit, Prenda, Etiqueta

class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = '__all__'  # Ajusta según los campos que necesites

class OutfitSerializer(serializers.ModelSerializer):
    prendas = PrendaSerializer(many=True, read_only=True)  # Incluir las prendas en el outfit

    class Meta:
        model = Outfit
        fields = '__all__'


# from rest_framework import serializers
# from .models import Etiqueta, Prenda  # Ajusta a tus modelos

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

