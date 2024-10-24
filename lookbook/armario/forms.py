from django import forms
from .models import Outfit, Prenda

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['foto', 'etiqueta']

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['nombre', 'enlace_compra', 'tipo']