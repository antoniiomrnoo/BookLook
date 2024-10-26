from django import forms
from .models import Outfit, Prenda
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['foto', 'etiqueta']

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = ['nombre', 'enlace_compra', 'tipo']


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']