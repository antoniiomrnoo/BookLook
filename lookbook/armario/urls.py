from django.urls import path, include
from .views import OutfitListView, OutfitDeleteView
from django.conf.urls.static import static
from django.conf import settings
from .views import OutfitCreateView
from . import views
from django.contrib.auth import views as auth_views
from .views import logout_view

urlpatterns = [
    path('lista_outfits/', OutfitListView.as_view(), name='outfit-list'),
    path('agregar/', OutfitCreateView.as_view(), name='agregar_outfit'),
    path('outfits/<int:pk>/', views.detalles, name='outfit-detalles'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),  # URL para la vista de edición
    path('outfits/<int:pk>/editar/', views.editar_outfit, name='editar-outfit'),
    path('eliminar/<int:pk>/', OutfitDeleteView.as_view(), name='eliminar_outfit'),
    path('outfit/<int:pk>/valorar/', views.valorar_outfit, name='valorar-outfit'),
    path('', views.carrusel_view, name='bienvenida'),
    path('mis-outfits/', views.user_outfits, name='user_outfits'),

    path('api/', include('armario.urls_api'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)