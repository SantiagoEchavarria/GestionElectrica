from django import forms 
from .models import Hogar, Dispositivo

class HogarForm(forms.ModelForm):
    class Meta:
        model=Hogar
        fields = ["nombre", "direccion"]
        
class DispositivoForm(forms.ModelForm):
    class Meta:
        model=Dispositivo
        fields = ["nombre", "tipo", "consumo_watts","hogar", "estado"]