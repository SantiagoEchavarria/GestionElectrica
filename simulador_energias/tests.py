from django.test import TestCase
from .models import Consumo
from datetime import date
import numpy as np
from dispositivos.models import Dispositivo, TipoDispositivo, Hogar, ParteHogar

class ConsumoTestCase(TestCase):
    def setUp(self):
        """ Configuración inicial de los objetos para el test """
        # Crear un hogar
        self.hogar = Hogar.objects.create(nombre="Casa de Prueba", direccion="Calle 123")

        # Crear una parte del hogar
        self.parte_hogar = ParteHogar.objects.create(nombre="Sala", hogar=self.hogar)

        # Crear un tipo de dispositivo
        self.tipo_dispositivo = TipoDispositivo.objects.create(
            nombre="Horno electrico",
            rango_consumo_min=700,
            rango_consumo_max=1200,
            descripcion="Microondas de cocina"
        )

        # Crear un dispositivo
        self.dispositivo = Dispositivo.objects.create(
            nombre="Horno electrico",
            tipo=self.tipo_dispositivo,
            consumo_watts=1000,  # 1 kW
            partehogar=self.parte_hogar,
            estado="encendido"
        )

        # Crear una instancia de Consumo
        self.consumo = Consumo(
            fecha_inicio=date(2024, 3, 1),
            fecha_fin=date(2024, 3, 3)
        )

    def test_calculo_consumo(self):
        """ Verifica que el método calcular_consumo retorna una matriz válida """
        matriz_consumo = self.consumo.calcular_consumo(self.dispositivo.nombre)

        # Imprimir la matriz de consumo para depuración
        print("\nMatriz de Consumo:" + self.dispositivo.tipo.nombre)
        print(matriz_consumo)

        
        matriz_consumo = self.consumo.calcular_consumo(self.dispositivo.nombre)

        # La salida debe ser un array de numpy
        self.assertIsInstance(matriz_consumo, np.ndarray, "La salida debe ser una matriz numpy")

        # La matriz debe tener 3 columnas (consumo, hora del evento, duración)
        if matriz_consumo.size > 0:  # Solo si hay eventos registrados
            self.assertEqual(matriz_consumo.shape[1], 5, "La matriz debe tener 5 columnas")

        # Verificar que los valores de hora estén en el rango correcto (0-23)
        for fila in matriz_consumo:
            self.assertTrue(0 <= fila[3] <= 23, "La hora del evento debe estar entre 0 y 23")
        
        # Verificar que la duración sea mayor a 0
        for fila in matriz_consumo:
            self.assertTrue(fila[4] > 0, "El tiempo de duración debe ser mayor a 0")




