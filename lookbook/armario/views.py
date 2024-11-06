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
            # Guarda el outfit primero
            outfit = outfit_form.save(commit=False)
            outfit.creador = request.user  # Asigna el usuario actual como creador
            outfit.save()  # Guarda el outfit

            # Guarda cada prenda asociada al outfit
            for prenda_form in prenda_forms:
                prenda = prenda_form.save(commit=False)  # No guardar aún
                prenda.outfit = outfit  # Asocia la prenda al outfit
                prenda.save()  # Guarda la prenda

            return redirect('outfit-list')

        return render(request, 'armario/agregar_outfit.html', {
            'outfit_form': outfit_form,
            'prenda_forms': prenda_forms,
        })


from .models import PerfilUsuario

@login_required
def perfil(request):
    perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)
    return render(request, 'perfil.html', {'perfil_usuario': perfil_usuario})


from .forms import PerfilUsuarioForm

@login_required
def editar_perfil(request):
    try:
        perfil_usuario = PerfilUsuario.objects.get(usuario=request.user)
    except PerfilUsuario.DoesNotExist:
        # Si no existe el perfil, puedes redirigir o crear uno
        return redirect('crear_perfil')  # Cambia esto según tu lógica
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige a la vista del perfil
    else:
        form = PerfilUsuarioForm(instance=perfil_usuario)
    
    return render(request, 'editar_perfil.html', {'form': form})


from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import DeleteView

# Vistas para editar y eliminar outfits solo por el creador

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from .models import Outfit, Prenda
from .forms import OutfitForm, PrendaForm

@login_required
def editar_outfit(request, pk):
    outfit = get_object_or_404(Outfit, pk=pk, creador=request.user)
    PrendaFormSet = inlineformset_factory(Outfit, Prenda, form=PrendaForm, extra=0, can_delete=True)
    outfit_form = OutfitForm(instance=outfit)
    prenda_formset = PrendaFormSet(instance=outfit)

    if request.method == 'POST':
        outfit_form = OutfitForm(request.POST, request.FILES, instance=outfit)
        prenda_formset = PrendaFormSet(request.POST, instance=outfit)
        
        if outfit_form.is_valid() and prenda_formset.is_valid():
            outfit_form.save()
            prenda_formset.save()
            return redirect('outfit-list')

    return render(request, 'armario/editar_outfit.html', {
        'outfit_form': outfit_form,
        'prenda_formset': prenda_formset,
    })

from django.views.generic import DeleteView
from django.urls import reverse_lazy

class OutfitDeleteView(DeleteView):
    model = Outfit
    template_name = 'armario/eliminar_outfit.html'  # Asegúrate de que este template exista
    success_url = reverse_lazy('outfit-list')  # Redirige a la lista de outfits después de la eliminación
