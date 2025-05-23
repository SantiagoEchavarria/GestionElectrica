from django.shortcuts import render
from django.http import JsonResponse
from dispositivos.models import Dispositivo
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
    
    # Preparar datos para el gráfico
    fechas_horas = [f"{registro.fecha} {registro.hora}:00" for registro in registros]
    consumos = [registro.consumo_electrico for registro in registros]
    dispositivo = registros[0].dispositivo  # Asumimos que todos tienen el mismo dispositivo
    
    # Crear el gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(fechas_horas, consumos, marker='o', linestyle='-', color='b')
    plt.title(f'Consumo eléctrico para {dispositivo} (Registro ID: {registro_id})')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Consumo eléctrico (kWh)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    
    # Convertir el gráfico a imagen para mostrar en HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    graphic = base64.b64encode(image_png).decode('utf-8')
    
    # Cerrar la figura para liberar memoria
    plt.close()
    
    context = {
        'graphic': graphic,
        'dispositivo': dispositivo,
        'registro_id': registro_id,
        'total_consumo': sum(consumos),
        'registros_count': len(registros),
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