import random
from django.db import models
import numpy as np
from dispositivos.models import Dispositivo
class Consumo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    energia_consumida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_consumo(self, dispositivo):
        consumo_diario = {
            'horno_electrico': {'Numero_de_eventos': (1, 3), 'Tiempo_promedio_evento': (15, 45)},  
            'lampara_led': {'Numero_de_eventos': (1, 5), 'Tiempo_promedio_evento': (60, 300)},  
            'cargador_celular': {'Numero_de_eventos': (1, 3), 'Tiempo_promedio_evento': (60, 180)},  
            'ventilador': {'Numero_de_eventos': (1, 2), 'Tiempo_promedio_evento': (120, 360)},  
            'aire_acondicionado': {'Numero_de_eventos': (1, 2), 'Tiempo_promedio_evento': (240, 480)},  
            'microondas': {'Numero_de_eventos': (1, 3), 'Tiempo_promedio_evento': (10, 30)},  
            'computadora_portatil': {'Numero_de_eventos': (1, 2), 'Tiempo_promedio_evento': (180, 300)},  
            'televisor_led': {'Numero_de_eventos': (1, 3), 'Tiempo_promedio_evento': (120, 300)},  
            'lavadora': {'Numero_de_eventos': (1, 2), 'Tiempo_promedio_evento': (30, 60)},  
            'nevera': {'Numero_de_eventos': (20, 24), 'Tiempo_promedio_evento': (30, 60)}  
        }

        dias = (self.fecha_fin - self.fecha_inicio).days + 1
        if dias < 1:
            return np.array([])  

        try:
            dispositivo_obj = Dispositivo.objects.get(nombre=dispositivo)  
        except Dispositivo.DoesNotExist:
            return np.array([])  

        if dispositivo_obj.nombre in consumo_diario:
            num_eventos_min, num_eventos_max = consumo_diario[dispositivo_obj.nombre]['Numero_de_eventos']
            tiempo_min, tiempo_max = consumo_diario[dispositivo_obj.nombre]['Tiempo_promedio_evento']

            matriz_consumo = []
            for _ in range(dias):
                num_eventos = random.randint(num_eventos_min, num_eventos_max)
                for _ in range(num_eventos):
                    tiempo_evento = random.randint(tiempo_min, tiempo_max)
                    hora_evento = random.randint(0, 23)  
                    
                    consumo_electrico = (tiempo_evento / 60) * dispositivo_obj.potencia  
                    
                    matriz_consumo.append([consumo_electrico, hora_evento, tiempo_evento])

            return np.array(matriz_consumo)

        return np.array([]) 
    
    def save(self, *args, **kwargs):
        self.energia_consumida = self.calcular_consumo()  # Calcular antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_dispositivo_display()} - {self.energia_consumida} kWh"