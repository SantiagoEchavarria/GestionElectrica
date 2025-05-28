from django.contrib import admin
from .models import Consumo, RegistroConsumo

admin.site.register(RegistroConsumo)
admin.site.register(Consumo)