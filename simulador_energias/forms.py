from django import forms 
from .models import Consumo

class ConsumoForm(forms.ModelForm):
    class Meta:
        model= Consumo
        fields= ["fecha_inicio", "fecha_fin"]