from django.urls import path
from .views import OutfitListView
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)