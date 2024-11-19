from django.urls import path
from .views import PrendaListCreateView, PrendaDetailView, EtiquetaListCreateView, EtiquetaDetailView, OutfitDetailView

urlpatterns = [
    # path('etiquetaapi/', EtiquetaListCreateView.as_view, name='etiqueta-api'),
    # path('etiquetaapi/<int:pk>/', EtiquetaDetailView.as_view, name='etiqueta-d'),
    # path('prendaapi/', PrendaListCreateView.as_view, name='prenda-api'),
    # path('prendaapi/<int:pk>/', PrendaDetailView.as_view, name='prenda-d'),
    path('outfitaapi/<int:pk>/', OutfitDetailView.as_view(), name='outfit-detail'),
]


#(Petición API)
#curl -X GET http://localhost:8000/api/outfitaapi/14/ 