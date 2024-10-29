from django.contrib import admin
from .models import Etiqueta, Outfit, Prenda

# Register your models here.

class PrendaInline(admin.TabularInline):  # Usa TabularInline para que aparezcan las prendas en forma de tabla
    model = Prenda
    extra = 1  # Número de campos adicionales para añadir nuevas prendas

# Registro de los modelos en el panel de administración
@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Outfit)
class OutfitAdmin(admin.ModelAdmin):
    list_display = ('id', 'etiqueta', 'creado_en')
    list_filter = ('etiqueta', 'creado_en')
    search_fields = ('id', 'etiqueta__nombre')
    inlines = [PrendaInline]  # Agregar el formulario en línea para prendas

@admin.register(Prenda)
class PrendaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'enlace_compra', 'outfit')
    list_filter = ('tipo', 'outfit__etiqueta')
    search_fields = ('nombre', 'outfit__etiqueta__nombre', 'tipo')


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario

# Define un Inline para PerfilUsuario
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Información Personal'

# Define una clase para el usuario que incluya el Inline de PerfilUsuario
class UsuarioAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)

# Re-registra el modelo User usando el nuevo administrador
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
