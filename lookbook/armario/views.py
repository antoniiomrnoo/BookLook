from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .models import Outfit, Etiqueta, Prenda
from .forms import OutfitForm, PrendaForm 
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view(request):
    return render(request, 'armario/bienvenida.html')

class OutfitListView(ListView):
    model = Outfit
    template_name = 'armario/lista_outfits.html'  # Ruta al template que mostrarás
    context_object_name = 'outfits'  # Nombre de la variable para acceder a los outfits en el template
    paginate_by = 10  # Opcional: Si quieres paginación, muestra 10 outfits por página (ajustable)


def detalles(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk)
    return render(request, 'armario/outfit_detalles.html', {'outfit': outfit})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente al registrarse
            messages.success(request, 'Registro exitoso')
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = RegistroForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.mixins import LoginRequiredMixin

class OutfitCreateView(LoginRequiredMixin, View):
    login_url = 'login'  # Redirige a esta URL si el usuario no está autenticado

    def get(self, request):
        outfit_form = OutfitForm()
        prenda_forms = [PrendaForm(prefix=f'prenda_{i}') for i in range(3)]
        return render(request, 'armario/agregar_outfit.html', {
            'outfit_form': outfit_form,
            'prenda_forms': prenda_forms,
        })

    def post(self, request):
        outfit_form = OutfitForm(request.POST, request.FILES)
        prenda_forms = []

    # Procesar cada prenda desde el número máximo que has definido
        for i in range(10):  # Ajusta este número si deseas permitir más o menos prendas
            prenda_form = PrendaForm(request.POST, prefix=f'prenda_{i}')
            if prenda_form.is_valid():
                prenda_forms.append(prenda_form)

        if outfit_form.is_valid() and prenda_forms:
            outfit = outfit_form.save()

            for prenda_form in prenda_forms:
                prenda = prenda_form.save(commit=False)
                prenda.outfit = outfit
                prenda.save()

            return redirect('outfit-list')

        return render(request, 'armario/agregar_outfit.html', {
            'outfit_form': outfit_form,
            'prenda_forms': prenda_forms,
        })
