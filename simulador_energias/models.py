import random
from django.db import models
import numpy as np
from dispositivos.models import Dispositivo
from datetime import timedelta

class Consumo(models.Model):
    
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def calcular_consumo(self, dispositivo):
        # Diccionario con patrones de uso y rangos horarios
        consumo_diario = {
            'horno_electrico': {'lambda_eventos': 1.5, 'media_tiempo': 30, 'rango_horas': (10, 14)},  
            'lampara_led': {'lambda_eventos': 2.5, 'media_tiempo': 300, 'rango_horas': (18, 23)},  
            'cargador_celular': {'lambda_eventos': 1.2, 'media_tiempo': 180, 'rango_horas': (22, 6)},  
            'ventilador': {'lambda_eventos': 1.8, 'media_tiempo': 360, 'rango_horas': (12, 18)},  
            'aire_acondicionado': {'lambda_eventos': 1.1, 'media_tiempo': 480, 'rango_horas': (20, 6)},  
            'Microondas': {'lambda_eventos': 2, 'media_tiempo': 3, 'rango_horas': (7, 9)},  
            'computadora_portatil': {'lambda_eventos': 1.4, 'media_tiempo': 300, 'rango_horas': (9, 17)},  
            'televisor_led': {'lambda_eventos': 1.6, 'media_tiempo': 240, 'rango_horas': (18, 23)},  
            'Lavadora': {'lambda_eventos': 1.2, 'media_tiempo': 60, 'rango_horas': (8, 12)},  
            'nevera': {'lambda_eventos': 24, 'media_tiempo': 60, 'rango_horas': (0, 23)}  
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
        print("Tipo: "+dispositivo_obj.tipo.nombre)
        
        if dispositivo_obj.tipo.nombre in consumo_diario:
            datos_dispositivo = consumo_diario[dispositivo_obj.tipo.nombre]
            lambda_eventos = datos_dispositivo['lambda_eventos']
            media_tiempo = datos_dispositivo['media_tiempo']
            rango_horas = datos_dispositivo['rango_horas']

            print(f"Número de eventos: {lambda_eventos}")
            print(f"Media de tiempo: {media_tiempo}")
            print(f"Rango de uso: {rango_horas[0]} - {rango_horas[1]} horas")

            matriz_consumo = []
            fecha_actual = self.fecha_inicio

            for _ in range(dias):
                num_eventos = np.random.poisson(lambda_eventos)

                for _ in range(num_eventos):
                    tiempo_evento = int(np.random.exponential(scale=media_tiempo))
                    tiempo_evento = max(1, tiempo_evento)
                    
                    hora_evento = random.randint(rango_horas[0], rango_horas[1])
                    
                    consumo_electrico = (tiempo_evento / 60) * (float(dispositivo_obj.consumo_watts) / 1000)

                    matriz_consumo.append([dispositivo_obj.nombre, str(fecha_actual),  f"{consumo_electrico:.2f}", hora_evento, tiempo_evento])

                fecha_actual += timedelta(days=1)  
                
            matriz_consumo.sort(key=lambda x: (x[1], x[3]))
            return np.array(matriz_consumo, dtype=object)  # dtype=object para almacenar fechas como string

        return np.array([])  

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_dispositivo_display()} - {self.energia_consumida} kWh"
    
class RegistroConsumo(models.Model):
    consumo = models.ForeignKey(Consumo, on_delete=models.CASCADE, related_name="registros")
    dispositivo = models.CharField(max_length=50)
    fecha = models.DateField()
    consumo_electrico = models.FloatField()
    hora = models.IntegerField()
    duracion = models.IntegerField()