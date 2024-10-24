from django.urls import path
from .views import OutfitListView
from django.conf.urls.static import static
from django.conf import settings
from .views import OutfitCreateView

urlpatterns = [
    path('media/outfits/', OutfitListView.as_view(), name='outfit-list'),
    path('agregar/', OutfitCreateView.as_view(), name='agregar_outfit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)