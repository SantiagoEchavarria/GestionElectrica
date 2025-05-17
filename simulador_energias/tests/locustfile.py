from locust import HttpUser, task, between
from datetime import date
import random
import json

class CargaSimulador(HttpUser):
    wait_time = between(0.001, 0.01)  # entre solicitudes

    @task
    def verificar_consumo(self):
        # Simula fechas de consulta
        fecha_inicio = date(2025, 5, 1)
        fecha_fin = date(2025, 5, 10)

        # Simula un consumo_id existente en la base de datos
        consumo_id = random.randint(1, 10)

        # Envía solicitud al endpoint que evalúa el umbral 
        # Realiza el proceso de verificar_umbral(request, id): que esta en simulador_energias/views y a su vez
        #Este usa las funciones de utils.py del mismo modulo
        self.client.get(f"/api/consumo/{consumo_id}/verificar?inicio={fecha_inicio}&fin={fecha_fin}")
