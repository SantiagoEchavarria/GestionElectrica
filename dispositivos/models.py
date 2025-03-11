from django.db import models

class TipoDispositivo(models.Model):
    nombre = models.CharField(max_length=100)
    rango_consumo_min = models.DecimalField(max_digits=10, decimal_places=2)
    rango_consumo_max = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Hogar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
class ParteHogar(models.Model):
    nombre = models.CharField(max_length=100)
    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE, related_name="partes", default=1)

    def __str__(self):
        return f"{self.nombre} - {self.hogar.nombre}"
    

class Dispositivo(models.Model):
    ESTADO_CHOICES = [
        ('encendido', 'Encendido'),
        ('apagado', 'Apagado')
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoDispositivo, on_delete=models.RESTRICT)
    consumo_watts = models.DecimalField(max_digits=10, decimal_places=2)
    hogar = models.ForeignKey(Hogar, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='apagado')

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"