from django import forms 
from .models import Hogar, Dispositivo, TipoDispositivo, ParteHogar

class HogarForm(forms.ModelForm):
    class Meta:
        model=Hogar
        fields = ["nombre", "direccion"]
        
class ParteHogarForm(forms.ModelForm):
    class Meta:
        model=ParteHogar
        fields = ["nombre", "hogar"]
        
class DispositivoForm(forms.ModelForm):
    class Meta:
        model=Dispositivo
        fields = ["nombre", "tipo", "consumo_watts","partehogar", "estado"]


class TipoDispotivoForm(forms.ModelForm):
    class Meta:
        model = TipoDispositivo
        fields = ["nombre","rango_consumo_min","rango_consumo_max","descripcion"]