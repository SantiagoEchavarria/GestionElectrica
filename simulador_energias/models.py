import random
from django.db import models
import numpy as np
from dispositivos.models import Dispositivo
from datetime import timedelta

class Consumo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    energia_consumida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_consumo(self, dispositivo):
        consumo_diario = {
            'horno_electrico': {'lambda_eventos': 1.5, 'media_tiempo': 30},  
            'lampara_led': {'lambda_eventos': 2.5, 'media_tiempo': 300},  
            'cargador_celular': {'lambda_eventos': 1.2, 'media_tiempo': 180},  
            'ventilador': {'lambda_eventos': 1.8, 'media_tiempo': 360},  
            'aire_acondicionado': {'lambda_eventos': 1.1, 'media_tiempo': 480},  
            'microondas': {'lambda_eventos': 2.3, 'media_tiempo': 18},  
            'computadora_portatil': {'lambda_eventos': 1.4, 'media_tiempo': 300},  
            'televisor_led': {'lambda_eventos': 1.6, 'media_tiempo': 240},  
            'lavadora': {'lambda_eventos': 1.2, 'media_tiempo': 60},  
            'nevera': {'lambda_eventos': 24, 'media_tiempo': 60}  
        }

        dias = (self.fecha_fin - self.fecha_inicio).days + 1
        if dias < 1:
            return np.array([])  

        try:
            dispositivo_obj = Dispositivo.objects.get(nombre=dispositivo)  
            print(dispositivo_obj.nombre + " encontrado en la base de datos.")
        except Dispositivo.DoesNotExist:
            print(dispositivo + " NO encontrado en la base de datos.")
            return np.array([])  

        if dispositivo_obj.tipo.nombre in consumo_diario:
            lambda_eventos = consumo_diario[dispositivo_obj.tipo.nombre]['lambda_eventos']
            media_tiempo = consumo_diario[dispositivo_obj.tipo.nombre]['media_tiempo']
            print(f"Número de eventos: {lambda_eventos}")
            print(f"Media de tiempo: {media_tiempo}")

            matriz_consumo = []
            fecha_actual = self.fecha_inicio
            for _ in range(dias):
                num_eventos = np.random.poisson(lambda_eventos)

                for _ in range(num_eventos):
                    tiempo_evento = int(np.random.exponential(scale=media_tiempo))
                    tiempo_evento = max(1, tiempo_evento)
                    
                    hora_evento = random.randint(0, 23)

                    # Conversión de Decimal a float
                    consumo_electrico = (tiempo_evento / 60) * float(dispositivo_obj.consumo_watts)

                    # Agregar la fecha al registro
                    matriz_consumo.append([str(fecha_actual),  f"{consumo_electrico:.2f}", hora_evento, tiempo_evento])

                fecha_actual += timedelta(days=1)  # Avanzar al siguiente día

            return np.array(matriz_consumo, dtype=object)  # dtype=object para almacenar fechas como string

        return np.array([])  

    def save(self, *args, **kwargs):
        self.energia_consumida = self.calcular_consumo(self.dispositivo.nombre)  # Calcular antes de guardar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_dispositivo_display()} - {self.energia_consumida} kWh"
