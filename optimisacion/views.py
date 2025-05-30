import json
from django.shortcuts import render
from django.http import JsonResponse
from dispositivos.models import Dispositivo, TipoDispositivo
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from simulador_energias.models import Consumo, RegistroConsumo
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from django.db.models import Sum
@login_required
def grafico_consumo_por_registro(request, registro_id):
    # Obtener todos los registros con el registro_id especificado
    registros = RegistroConsumo.objects.filter(registro_id=registro_id).order_by('fecha', 'hora')

    if not registros.exists():
        return render(request, 'error.html', {'message': 'No se encontraron registros con ese ID'})

    # Preparar datos para el gráfico de JavaScript
    fechas_horas = [f"{registro.fecha} {registro.hora}" for registro in registros]
    consumos = [registro.consumo_electrico for registro in registros]
    dispositivo = registros[0].dispositivo

    try:
        tipo_dispositivo = TipoDispositivo.objects.get(nombre=dispositivo)
        maximo = tipo_dispositivo.rango_consumo_max/1000
        minimo = tipo_dispositivo.rango_consumo_min/1000
        print("maximo " + str(maximo))
        print("minimo " + str(minimo))
    except TipoDispositivo.DoesNotExist:
        maximo = None
        minimo = None
        print(f"Advertencia: No se encontró TipoDispositivo para '{dispositivo}'.")

    context = {
        'fechas_horas': json.dumps(fechas_horas),
        'consumos': json.dumps(consumos),
        'dispositivo': dispositivo,
        'registro_id': registro_id,
        'total_consumo': sum(consumos),
        'registros_count': len(registros),
        'maximo': maximo,
        'minimo': minimo,
    }

    return render(request, 'grafico_consumo.html', context)


@login_required
def consumo_actual(request):
    dispositivos_activos = Dispositivo.objects.filter(estado='encendido')
    consumo_total = sum(d.consumo_watts for d in dispositivos_activos)

    detalles = [
        {
            'nombre': d.nombre,
            'consumo': float(d.consumo_watts),
            'ubicacion': d.partehogar.nombre
        }
        for d in dispositivos_activos
    ]

    data = {
        'cantidad_dispositivos': dispositivos_activos.count(),
        'consumo_total': float(consumo_total),
        'detalles': detalles
    }

    return JsonResponse(data)

@login_required
def vista_optimizacion(request):
    return render(request, 'optimizacion.html')