from django import forms
from .models import Outfit, Prenda
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilUsuario

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


class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label="Nombre", required=False)
    last_name = forms.CharField(label="Apellidos", required=False)
    email = forms.EmailField(label="Correo electrónico", required=False)

    class Meta:
        model = PerfilUsuario
        fields = ['numero_telefono', 'biografia', 'marca_favorita', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.usuario:
            self.fields['first_name'].initial = self.instance.usuario.first_name
            self.fields['last_name'].initial = self.instance.usuario.last_name
            self.fields['email'].initial = self.instance.usuario.email

    def save(self, *args, **kwargs):
        perfil = super(PerfilUsuarioForm, self).save(*args, **kwargs)
        
        # Actualiza los campos del User solo si están presentes
        if 'first_name' in self.cleaned_data:
            perfil.usuario.first_name = self.cleaned_data['first_name']
        if 'last_name' in self.cleaned_data:
            perfil.usuario.last_name = self.cleaned_data['last_name']
        if 'email' in self.cleaned_data:
            perfil.usuario.email = self.cleaned_data['email']
        
        perfil.usuario.save()  # Guarda los cambios en el usuario
        return perfil

