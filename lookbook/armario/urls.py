from django.urls import path
from .views import OutfitListView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('outfits/', OutfitListView.as_view(), name='outfit-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)