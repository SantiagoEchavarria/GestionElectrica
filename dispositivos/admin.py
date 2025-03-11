from django.contrib import admin
from . models import TipoDispositivo, Dispositivo, Hogar, ParteHogar

admin.site.register(TipoDispositivo)
admin.site.register(ParteHogar)
admin.site.register(Dispositivo)
admin.site.register(Hogar)