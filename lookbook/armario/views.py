from django.shortcuts import render
from django.views.generic import ListView
from .models import Outfit

# Create your views here.

class OutfitListView(ListView):
    model = Outfit
    template_name = 'armario/lista_outfits.html'  # Ruta al template que mostrarás
    context_object_name = 'outfits'  # Nombre de la variable para acceder a los outfits en el template
    paginate_by = 10  # Opcional: Si quieres paginación, muestra 10 outfits por página (ajustable)

