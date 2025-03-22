import random
from django.db import models
import numpy as np
from dispositivos.models import Dispositivo

class Consumo(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    energia_consumida = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calcular_consumo(self, dispositivo_nombre):
        """Calcula el consumo de un dispositivo en un rango de fechas."""
        
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
            dispositivo_obj = Dispositivo.objects.get(nombre=dispositivo_nombre)
            print(f"{dispositivo_obj.nombre} encontrado en la base de datos.")
        except Dispositivo.DoesNotExist:
            print(f"El dispositivo {dispositivo_nombre} no existe.")
            return np.array([])  

        tipo_dispositivo = dispositivo_obj.tipo.nombre.lower()
        if tipo_dispositivo in consumo_diario:
            lambda_eventos = consumo_diario[tipo_dispositivo]['lambda_eventos']
            media_tiempo = consumo_diario[tipo_dispositivo]['media_tiempo']
            print(f"Número de eventos: {lambda_eventos}")
            print(f"Media de tiempo: {media_tiempo}")    

            matriz_consumo = []
            for _ in range(dias):
                num_eventos = np.random.poisson(lambda_eventos)

                for _ in range(num_eventos):
                    tiempo_evento = max(1, int(np.random.exponential(scale=media_tiempo)))  
                    hora_evento = random.randint(0, 23)
                    consumo_electrico = (tiempo_evento / 60) * float(dispositivo_obj.consumo_watts)  

                    matriz_consumo.append([consumo_electrico, hora_evento, tiempo_evento])

            return np.array(matriz_consumo)

        return np.array([])  
    
    def save(self, *args, **kwargs):
        """Calcula y guarda el consumo antes de almacenar el objeto."""
        if self.energia_consumida is None:  
            self.energia_consumida = 0  # Puedes inicializar con 0 si no se calcula aún
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consumo entre {self.fecha_inicio} y {self.fecha_fin} - {self.energia_consumida} kWh"
