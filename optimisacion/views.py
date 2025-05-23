from django.shortcuts import render
from django.http import JsonResponse
from dispositivos.models import Dispositivo
from django.contrib.auth.decorators import login_required




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