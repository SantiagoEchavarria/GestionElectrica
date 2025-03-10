from django.contrib import admin
from .models import Usuario
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "nombre", "is_staff", "is_superuser"]
    search_fields = ["email", "nombre"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Información personal", {"fields": ("nombre", "telefono", "fecha_nacimiento")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nombre", "password1", "password2"),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)
