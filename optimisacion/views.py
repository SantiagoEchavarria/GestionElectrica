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
from collections import Counter
import pandas as pd
import seaborn as sns
from io import BytesIO
from django.core.serializers.json import DjangoJSONEncoder


def obtener_datos_lineas_multiples2():
    registros = RegistroConsumo.objects.all().order_by('fecha', 'hora')

    if not registros.exists():
        return {
            'lineas_multiples_labels': json.dumps([], cls=DjangoJSONEncoder),
            'lineas_multiples_series': json.dumps({}, cls=DjangoJSONEncoder)
        }

    data = {}
    labels = []

    for registro in registros:
        fecha_hora = f"{registro.fecha} {registro.hora:02}:00"
        if fecha_hora not in labels:
            labels.append(fecha_hora)
        dispositivo = str(registro.dispositivo)
        data.setdefault(dispositivo, {})[fecha_hora] = registro.consumo_electrico

    # Asegurar que todos los dispositivos tengan valores para todas las fechas
    for dispositivo in data:
        for label in labels:
            data[dispositivo].setdefault(label, 0)

    # Formatear datos para Chart.js
    datasets = {
        dispositivo: [data[dispositivo][label] for label in labels]
        for dispositivo in data
    }

    return {
        'lineas_multiples_labels': json.dumps(labels, cls=DjangoJSONEncoder),
        'lineas_multiples_series': json.dumps(datasets, cls=DjangoJSONEncoder),
    }

def generar_grafico_lineas_multiples():
    registros = RegistroConsumo.objects.all()

    if not registros.exists():
        return {'lineas_multiples_image': None}

    data = {
       'fecha_hora': [
            f"{registro.fecha} {registro.hora:02}:00:00"
            for registro in registros
        ],

        'consumo': [registro.consumo_electrico for registro in registros],
        'dispositivo': [registro.dispositivo for registro in registros],
    }

    df = pd.DataFrame(data)
    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])  # ya está en formato correcto

    plt.figure(figsize=(14, 6))

    for dispositivo in df['dispositivo'].unique():
        subset = df[df['dispositivo'] == dispositivo]
        plt.plot(subset['fecha_hora'], subset['consumo'], label=dispositivo)

    plt.xlabel('Fecha y Hora')
    plt.ylabel('Consumo Eléctrico (kWh)')
    plt.title('Consumo Eléctrico por Dispositivo')
    plt.legend()
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    lineas_multiples_base64 = base64.b64encode(image_png).decode('utf-8')

    return {'lineas_multiples_image': lineas_multiples_base64}

def generar_matriz_calor(registro_id):
    registros = RegistroConsumo.objects.filter(registro_id=registro_id)

    if not registros.exists():
        return {'heatmap_image': None}

    data = {
        'fecha': [registro.fecha for registro in registros],
        'hora': [registro.hora for registro in registros],
        'consumo': [registro.consumo_electrico for registro in registros]
    }

    df = pd.DataFrame(data)
    pivot = df.pivot_table(index='hora', columns='fecha', values='consumo', aggfunc='sum', fill_value=0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5)
    plt.title('Matriz de Calor de Consumo Eléctrico')
    plt.xlabel('Fecha')
    plt.ylabel('Hora')

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    heatmap_base64 = base64.b64encode(image_png).decode('utf-8')

    return {'heatmap_image': heatmap_base64}
    
    
@login_required
def grafico_consumo_por_registro(request, registro_id):
    usuario = request.user
    registros = RegistroConsumo.objects.filter(registro_id=registro_id).order_by('fecha', 'hora')

    if not registros.exists():
        return render(request, 'error.html', {'message': 'No se encontraron registros con ese ID'})

    fechas_horas = [f"{registro.fecha} {registro.hora:02}:00:00" for registro in registros]
    consumos = [registro.consumo_electrico for registro in registros]
    dispositivo = registros[0].dispositivo

    try:
        tipo_dispositivo = TipoDispositivo.objects.get(nombre=dispositivo)
        maximo = tipo_dispositivo.rango_consumo_max / 1000
        minimo = tipo_dispositivo.rango_consumo_min / 1000
    except TipoDispositivo.DoesNotExist:
        maximo = None
        minimo = None
        print(f"Advertencia: No se encontró TipoDispositivo para '{dispositivo}'.")

    # Identificar consumos que superan el máximo
    registros_superan_maximo = []
    if maximo is not None:
        for registro in registros:
            consumo_kw = registro.consumo_electrico
            if consumo_kw > maximo:
                registros_superan_maximo.append({
                    'fecha_hora': f"{registro.fecha} {registro.hora:02}:00:00",
                    'consumo': consumo_kw
                })

    all_registros = RegistroConsumo.objects.all()
    device_counts = Counter(reg.dispositivo for reg in all_registros)
    pie_chart_labels = list(device_counts.keys())
    pie_chart_data = list(device_counts.values())

    # Matriz de calor
    heatmap_context = generar_matriz_calor(registro_id)
    heatmap_image = heatmap_context.get('heatmap_image')

    context = {
        'usuario': usuario,
        'fechas_horas': json.dumps(fechas_horas),
        'consumos': json.dumps(consumos),
        'dispositivo': dispositivo,
        'registro_id': registro_id,
        'total_consumo': sum(consumos),
        'registros_count': len(registros),
        'maximo': maximo,
        'minimo': minimo,
        'pie_chart_labels': json.dumps(pie_chart_labels),
        'pie_chart_data': json.dumps(pie_chart_data),
        'heatmap_image': heatmap_image,
        'registros_superan_maximo': registros_superan_maximo,
    }
    context.update(obtener_datos_lineas_multiples2())

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