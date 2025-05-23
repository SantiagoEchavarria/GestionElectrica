import random
from django.db import models
import numpy as np
from dispositivos.models import Dispositivo
from datetime import timedelta
import holidays
import uuid
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime

class Consumo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def calcular_consumo(self, dispositivo):
        consumo_diario = {
            'Horno electrico': {'lambda_eventos': 1.5, 'media_tiempo': 30, 'rango_horas': (10, 14)},  
            'Lampara led': {'lambda_eventos': 2.5, 'media_tiempo': 300, 'rango_horas': (18, 23)},  
            'Cargador celular': {'lambda_eventos': 2, 'media_tiempo': 120, 'rango_horas': (6, 22)},  
            'Ventilador': {'lambda_eventos': 1.8, 'media_tiempo': 360, 'rango_horas': (12, 18)},  
            'Aire acondicionado': {'lambda_eventos': 1.1, 'media_tiempo': 480, 'rango_horas': (20, 6)},  
            'Microondas': {'lambda_eventos': 2, 'media_tiempo': 3, 'rango_horas': (7, 9)},  
            'Computadora portatil': {'lambda_eventos': 1.4, 'media_tiempo': 300, 'rango_horas': (9, 17)},  
            'Televisor led': {'lambda_eventos': 1.6, 'media_tiempo': 240, 'rango_horas': (18, 23)},  
            'Lavadora': {'lambda_eventos': 1.2, 'media_tiempo': 60, 'rango_horas': (8, 12)},  
            'Nevera': {'lambda_eventos': 1, 'media_tiempo': 1440, 'rango_horas': (1,1)}  
        }

        dias = (self.fecha_fin - self.fecha_inicio).days + 1
        if dias < 1:
            return np.array([])

        try:
            dispositivo_obj = Dispositivo.objects.get(nombre=dispositivo)
        except Dispositivo.DoesNotExist:
            return np.array([])
        
        # Generar un único ID para todos los registros de esta llamada
        consumo_id  = uuid.uuid4()
        
        if dispositivo_obj.tipo.nombre in consumo_diario:
            datos_dispositivo = consumo_diario[dispositivo_obj.tipo.nombre]
            lambda_eventos = datos_dispositivo['lambda_eventos']
            media_tiempo = datos_dispositivo['media_tiempo']
            rango_horas = datos_dispositivo['rango_horas']

            matriz_consumo = []
            fecha_actual = self.fecha_inicio
            festivos = holidays.Colombia(years=range(self.fecha_inicio.year, self.fecha_fin.year + 1))

            for _ in range(dias):
                if dispositivo_obj.tipo.nombre.lower() == 'nevera':
                    consumo_por_hora = (media_tiempo / 60) * (float(dispositivo_obj.consumo_watts) / 1000)
                    matriz_consumo.append([
                        dispositivo_obj.nombre, 
                        str(fecha_actual), 
                        f"{consumo_por_hora:.3f}", 
                        24, 
                        media_tiempo,
                        str(consumo_id )
                    ])
                else:
                    num_eventos = np.random.poisson(lambda_eventos)
                    if fecha_actual.weekday() >= 5 or fecha_actual in festivos:
                        num_eventos += 1
                    
                    for _ in range(num_eventos):
                        tiempo_evento = int(np.random.exponential(scale=media_tiempo))
                        tiempo_evento = max(1, tiempo_evento)
                        hora_evento = random.randint(rango_horas[0], rango_horas[1])
                        
                        if dispositivo_obj.tipo.nombre.lower() == 'lampara_led':
                            if hora_evento < 20:
                                tiempo_evento = max(1, tiempo_evento // 2)
                            elif hora_evento >= 22:
                                tiempo_evento = min(media_tiempo, tiempo_evento * 1.5)

                        consumo_electrico = (tiempo_evento / 60) * (float(dispositivo_obj.consumo_watts) / 1000)
                        matriz_consumo.append([
                            dispositivo_obj.nombre, 
                            str(fecha_actual), 
                            f"{consumo_electrico:.3f}", 
                            hora_evento, 
                            tiempo_evento,
                            str(consumo_id )
                        ])
                
                fecha_actual += timedelta(days=1)
                
            matriz_consumo.sort(key=lambda x: (x[1], x[3]))  # Ordenar por fecha y hora
            return np.array(matriz_consumo, dtype=object)
        
        return np.array([])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consumo del {self.fecha_inicio} al {self.fecha_fin}"


class RegistroConsumo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consumo = models.ForeignKey(Consumo, on_delete=models.CASCADE, related_name="registros")
    dispositivo = models.CharField(max_length=50)
    fecha = models.DateField()
    consumo_electrico = models.FloatField()
    hora = models.IntegerField()
    duracion = models.IntegerField()
    registro_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dispositivo} - {self.fecha} - {self.registro_id}"

