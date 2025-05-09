from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
import re

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento', 'password1', 'password2']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre.strip()) == 0:
            raise ValidationError("El nombre es obligatorio.")
        if len(nombre) > 50:
            raise ValidationError("El nombre no debe tener más de 50 caracteres.")
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError("El correo electrónico debe contener un '@'.")
        if len(email) > 100:
            raise ValidationError("El correo electrónico no debe tener más de 100 caracteres.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{7,15}$', telefono):
            raise ValidationError("El teléfono debe tener solo números y entre 7 y 15 dígitos.")
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise ValidationError("Debe ingresar una fecha de nacimiento.")
        if fecha >= date.today():
            raise ValidationError("La fecha de nacimiento debe ser anterior a hoy.")
        return fecha

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'email', 'telefono', 'fecha_nacimiento']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre.strip()) == 0:
            raise ValidationError("El nombre es obligatorio.")
        if len(nombre) > 50:
            raise ValidationError("El nombre no debe tener más de 50 caracteres.")
        return nombre

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError("El correo electrónico debe contener un '@'.")
        if len(email) > 100:
            raise ValidationError("El correo electrónico no debe tener más de 100 caracteres.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{7,15}$', telefono):
            raise ValidationError("El teléfono debe tener solo números y entre 7 y 15 dígitos.")
        return telefono

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data.get('fecha_nacimiento')
        if not fecha:
            raise ValidationError("Debe ingresar una fecha de nacimiento.")
        if fecha >= date.today():
            raise ValidationError("La fecha de nacimiento debe ser anterior a hoy.")
        return fecha
