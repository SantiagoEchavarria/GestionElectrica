from django import forms 
from .models import Hogar

class HogarForm(forms.ModelForm):
    class Meta:
        model=Hogar
        fields = ["nombre", "direccion"]