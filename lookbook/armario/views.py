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

from django.views.generic import ListView
from django.db.models import Q
from .models import Outfit

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView
from .models import Outfit
from django.db.models import Avg
from django.views.generic import ListView
from django.db.models import Q
from .models import Outfit

class OutfitListView(ListView):
    model = Outfit
    template_name = 'armario/lista_outfits.html'  # Ruta al template que mostrarás
    context_object_name = 'outfits'  # Nombre de la variable para acceder a los outfits en el template
    paginate_by = 10  # Muestra 10 outfits por página

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')  # Obtiene el término de búsqueda
        if query:
            queryset = queryset.filter(
                Q(etiqueta__nombre__icontains=query) |
                Q(creador__username__icontains=query) |
                Q(prendas__nombre__icontains=query)
            ).distinct()  # Elimina duplicados por relaciones
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')  # Añade el término de búsqueda al contexto

        # Calcular el promedio de valoración para cada outfit
        for outfit in context['outfits']:
            promedio_valoracion = outfit.valoraciones.aggregate(promedio=Avg('valor'))['promedio'] or 0
            outfit.valoracion_promedio = round(promedio_valoracion, 1)

        return context


from django.db.models import Avg
from django.shortcuts import redirect
from armario.models import Valoracion  # Asegúrate de importar el modelo adecuado

def detalles(request, pk):
    """
    Muestra los detalles de un outfit específico y permite valorar.
    """
    outfit = get_object_or_404(Outfit, pk=pk)
    promedio_valoracion = outfit.valoraciones.aggregate(promedio=Avg('valor'))['promedio'] or 0

    # Manejar el envío de una valoración
    if request.method == 'POST':
        valor = request.POST.get('valor')
        if valor and request.user.is_authenticated:
            Valoracion.objects.create(outfit=outfit, usuario=request.user, valor=valor)
            return redirect('outfit-detalles', pk=pk)

    return render(request, 'armario/outfit_detalles.html', {
        'outfit': outfit,
        'promedio_valoracion': round(promedio_valoracion, 1)
    })


def registro(request):
    """
    Permite a los usuarios registrarse.
    """
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

# class OutfitListView(ListView):
#     model = Outfit
#     template_name = 'armario/lista_outfits.html'  # Ruta al template que mostrarás
#     context_object_name = 'outfits'  # Nombre de la variable para acceder a los outfits en el template
#     paginate_by = 10  # Opcional: Si quieres paginación, muestra 10 outfits por página (ajustable)


# def detalles(request, pk):
#     outfit = get_object_or_404(Outfit, pk=pk)
#     return render(request, 'armario/outfit_detalles.html', {'outfit': outfit})


# def registro(request):
#     if request.method == 'POST':
#         form = RegistroForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Inicia sesión automáticamente al registrarse
#             messages.success(request, 'Registro exitoso')
#             return redirect('home')  # Redirige a la página de inicio
#     else:
#         form = RegistroForm()
#     return render(request, 'registration/register.html', {'form': form})

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
from django.http import Http404

class OutfitDeleteView(DeleteView):
    model = Outfit
    template_name = 'armario/eliminar_outfit.html'
    success_url = reverse_lazy('outfit-list')

    def get_object(self, queryset=None):
        # Obtén el objeto
        obj = super().get_object(queryset)
        # Verifica si el usuario es el creador
        if obj.creador != self.request.user:
            raise Http404("No tienes permiso para eliminar este outfit")
        return obj

#API

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Prenda, Etiqueta
from .filters import PrendaFilter, EtiquetaFilter
from .serializers import EtiquetaSerializer, PrendaSerializer, OutfitSerializer
from django_filters import rest_framework as filters

class EtiquetaListCreateView(generics.ListCreateAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    filter_backends=[filters.DjangoFilterBackend]
    filter_backends= EtiquetaFilter

class PrendaListCreateView(generics.ListCreateAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
    filter_backends=[filters.DjangoFilterBackend]
    filter_backends= PrendaFilter

class PrendaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer

class EtiquetaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer

class OutfitDetailView(generics.RetrieveAPIView):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer


#Valoraciones

from django.http import JsonResponse
from .models import Valoracion

@login_required
def valorar_outfit(request, pk):
    """
    Permite a los usuarios valorar un outfit.
    """
    if request.method == 'POST':
        outfit = get_object_or_404(Outfit, pk=pk)
        valor = int(request.POST.get('valor', 0))
        if valor < 1 or valor > 5:
            return JsonResponse({'error': 'Valoración no válida'}, status=400)

        # Crea o actualiza la valoración del usuario
        valoracion, creada = Valoracion.objects.update_or_create(
            outfit=outfit, usuario=request.user, defaults={'valor': valor}
        )
        return JsonResponse({'success': 'Valoración registrada con éxito', 'valor': valoracion.valor})

    return JsonResponse({'error': 'Método no permitido'}, status=405)




from django.shortcuts import render
from django.db.models import Avg
from armario.models import Outfit

def carrusel_view(request):
    # Obtén los 5 outfits con mayor puntuación promedio
    outfits_mejor_valorados = Outfit.objects.annotate(
        promedio_valoracion=Avg('valoraciones__valor')
    ).order_by('-promedio_valoracion')[:5]

    return render(request, 'armario/bienvenida.html', {
        'outfits_mejor_valorados': outfits_mejor_valorados
    })



from django.shortcuts import render
from .models import Outfit  # Asegúrate de que Outfit sea el nombre correcto de tu modelo de outfit

def user_outfits(request):
    if request.user.is_authenticated:
        outfits = Outfit.objects.filter(creador=request.user)  # Filtra los outfits del usuario
        return render(request, 'user_outfits.html', {'outfits': outfits})
    else:
        return redirect('login')  # Redirige a login si el usuario no está autenticado
